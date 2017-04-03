"""
General helper scripts
Not to be used for analysis or called from production code!
"""

def generate_feature_mapping(out_file='mapping.txt'):

    hands = ['left', 'right']
    fingers = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bones = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    joints = ['direction', 'next_joint', 'prev_joint']
    coords = ['x', 'y', 'z']
    rotations = ['pitch', 'yaw', 'roll']

    f = open(out_file, 'w')

    for hand in hands:
        for finger in fingers:
            for bone in bones:
                for joint in joints:
                    for coord in coords:
                        feat_name = ['frame',
                                    'hands',
                                    hand,
                                    'fingers',
                                    finger,
                                    'bones',
                                    bone,
                                    joint,
                                    coord]
                        f.write('.'.join(feat_name) + '\n')
        for coord in coords:
            f.write('.'.join(['frame', 'hands', hand, 'palm_pos', coord]) + '\n')
        for rot in rotations:
            f.write('.'.join(['frame', 'hands', hand, rot]) + '\n')

    f.close()
