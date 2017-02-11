import Leap
import sys
import thread
import time
import numpy as np
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class RawDataListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    data = None

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        data_frame = []
        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        # frame.id, frame.timestamp, len(frame.hands), len(frame.fingers),
        # len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            if hand.is_left is False:
                # handType = "Left hand" if hand.is_left else "Right hand"
                #
                # print "  %s, id %d, position: %s" % (
                #     handType, hand.id, hand.palm_position)

                # Get the hand's normal vector and direction
                normal = hand.palm_normal
                direction = hand.direction

                # Calculate the hand's pitch, roll, and yaw angles
                # print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                #     direction.pitch * Leap.RAD_TO_DEG,
                #     normal.roll * Leap.RAD_TO_DEG,
                #     direction.yaw * Leap.RAD_TO_DEG)
                # data_frame.append()
                data_frame += normal.to_float_array() + direction.to_float_array()
                # Get arm bone
                arm = hand.arm
                # print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                #     arm.direction,
                #     arm.wrist_position,
                #     arm.elbow_position)
                data_frame += arm.direction.to_float_array() + arm.wrist_position.to_float_array() + \
                    arm.elbow_position.to_float_array()

                # Get fingers
                for finger in hand.fingers:

                    # print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                    #     self.finger_names[finger.type],
                    #     finger.id,
                    #     finger.length,
                    #     finger.width)
                    data_frame += [finger.length, finger.width]
                    # Get bones
                    for b in range(0, 4):
                        bone = finger.bone(b)
                        # print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                        #     self.bone_names[bone.type],
                        #     bone.prev_joint,
                        #     bone.next_joint,
                        #     bone.direction)
                        data_frame += bone.prev_joint.to_float_array() + bone.next_joint.to_float_array() + \
                            bone.direction.to_float_array()
                # print type(normal), type(direction), type(direction.pitch)
                # print type(direction.to_float_array())
                # print direction.to_float_array()
        # print data_frame
        # self.data.append(data_frame)
        # if the global data object is None and current frame is not empty,
        if self.data is None and data_frame:
            print "fistpass"
            self.data = np.array(data_frame)
        elif self.data is not None and data_frame:
            # self.data.vstack(data_frame)
            print self.data.shape, len(data_frame)
            self.data = np.vstack((self.data, data_frame))

    def get_data(self):
        # return np.array(self.data)
        return self.data

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"


def main():
    listener = RawDataListener()
    controller = Leap.Controller()

    # r = raw_input("Enter to start\n")
    # if r ==
    # controller.add_listener(listener)
    data = None

    started = False
    while True:
        r = raw_input("Enter to start, s to stop")
        if not r and not started:
            controller.add_listener(listener)
            started = True
        elif r == 's':
            break
        elif not r and started:
            data = listener.get_data()
            controller.remove_listener(listener)
            started = False

    # print len(data), len(data[0])
    print data
if __name__ == '__main__':
    main()
