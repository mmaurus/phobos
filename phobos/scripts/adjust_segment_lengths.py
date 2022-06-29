#!python3
import yaml
import phobos

def can_be_used():
    import yaml

    return True


def cant_be_used_msg():
    return "Unknown error!"


INFO = 'Test the latest model using a CI-pipeline.'


def update_segment(robot, segment):
    parent = segment.parent
    child = segment.child
    axis = segment.axis
    new_length = segment.length
    new_mass = segment.mass

    coupled_parent = segment.coupled_parent
    coupled_child = segment.coupled_child
    coupled_axis = segment.coupled_axis

    sign =  1.0 if (axis > 0) else (-1.0 if (axis < 0) else 0.0)
    #tf = robot.getJointTransform(parent, child)
    tf = [3][3]
    idx = int(sign * axis -1)
    old_length = tf[3,0:2][idx]
    #diff = sign * new_length - old_length
    scale = (sign * new_length) / old_length

    link_name = "todo"

    if (new_mass != None):
        robot.links[link_name].intertials.mass = new_mass

    if (scale != 1.0):
        #adjust length
        robot.scale_link(link_name, scale)

    robot.links[link_name].intertials = phobos.calculate_intertials()


    

def main(args):
    import sys

    import argparse
    import os

    parser = argparse.ArgumentParser(description=INFO, prog="phobos "+os.path.basename(__file__)[:-3])
    parser.add_argument('config_file', type=str, help='Path to the config file', default="test_config.yml")
    parser.add_argument('urdf_file', type=str, help="Path to the urdf file")

    args = parser.parse_args(args)

    if not os.path.isfile(args.config_file):
        parser.print_help()
        raise Exception("Config file not found!")
    config = yaml.parse(args.config_file)


    if not os.path.isfile(args.urdf_file):
        parser.print_help()
        raise Exception("Urdf file not found!")

    robot = phobos.Robot(urdf=args.urdf_file)

    for segment in config:
        update_segment(robot, segment)


if __name__ == '__main__':
    import sys
    main(sys.argv)
