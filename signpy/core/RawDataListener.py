import inspect
import numpy as np
import os
import sys
import thread
curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
root_dir = os.path.abspath(os.path.join(curr_dir, '../'))
sys.path.insert(0, root_dir + '/lib')
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class RawDataListener(Leap.Listener):
    """
    This class reads data from the Leap and output a json file.
    """

    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def __init__(self, label):
        super(RawDataListener, self).__init__()
        self.frames = []
        self.label = label

    def on_init(self, controller):
        print('RawDataListener Initialized')

    def on_connect(self, controller):
        print('RawDataListener Connected.\n' +
              'Press ENTER to finish recording sample.')

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print('RawDataListener Disconnected')

    def on_exit(self, controller):
        print('RawDataListener Exited')

    def on_frame(self, controller):
        # TODO: Outsource this code to a dedicated writer Function

        # Get the most recent frame and report some basic information
        frame = controller.frame()
        coords = ['x', 'y', 'z']

        frame_data = {}
        frame_data['id'] = frame.id
        frame_data['label'] = self.label
        frame_data['timestamp'] = frame.timestamp
        frame_data['num_hands'] = len(frame.hands)
        frame_data['num_fingers'] = len(frame.fingers)
        frame_data['hands'] = {}

        # Get hands
        for hand in frame.hands:

            hand_type = 'left' if hand.is_left else 'right'

            hand_data = {}
            hand_data['id'] = hand.id
            hand_data['palm_pos'] = {}
            for p in zip(coords, hand.palm_normal):
                hand_data['palm_pos'][p[0]] = p[1]

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            hand_data['pitch'] = direction.pitch * Leap.RAD_TO_DEG
            hand_data['roll'] = normal.roll * Leap.RAD_TO_DEG
            hand_data['yaw'] = direction.yaw * Leap.RAD_TO_DEG

            # Get arm bone
            arm = hand.arm
            arm_data = {}

            arm_data['direction'] = {}
            for p in zip(coords, arm.direction):
                arm_data['direction'][p[0]] = p[1]

            arm_data['wrist_pos'] = {}
            for p in zip(coords, arm.wrist_position):
                arm_data['wrist_pos'][p[0]] = p[1]

            arm_data['elbow_pos'] = {}
            for p in zip(coords, arm.elbow_position):
                arm_data['elbow_pos'][p[0]] = p[1]

            hand_data['fingers'] = {}

            # Get fingers
            for finger in hand.fingers:

                finger_type = self.finger_names[finger.type]

                finger_data = {}
                finger_data['id'] = finger.id
                finger_data['length'] = finger.length
                finger_data['width'] = finger.width
                finger_data['bones'] = {}

                # Get bones
                for b in xrange(0, len(self.bone_names)):
                    bone = finger.bone(b)
                    bone_type = self.bone_names[bone.type]

                    bone_data = {}

                    bone_data['prev_joint'] = {}
                    for p in zip(coords, bone.prev_joint):
                        bone_data['prev_joint'][p[0]] = p[1]

                    bone_data['next_joint'] = {}
                    for p in zip(coords, bone.next_joint):
                        bone_data['next_joint'][p[0]] = p[1]

                    bone_data['direction'] = {}
                    for p in zip(coords, bone.direction):
                        bone_data['direction'][p[0]] = p[1]

                    finger_data['bones'][bone_type] = bone_data

                hand_data['fingers'][finger_type] = finger_data

            frame_data['hands'][hand_type] = hand_data

        self.frames.append(frame_data)

    def get_data(self):
        return self.frames
