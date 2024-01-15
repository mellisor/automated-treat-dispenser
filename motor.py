import argparse
from stepper_motor import StepperMotor

parser = argparse.ArgumentParser()
parser.add_argument('steps_per_sec', type=float, help='Steps to take per second. 512 is a good number for me')
parser.add_argument('-r', '--reverse', action='store_true', help='Whether the motor should move in reverse')

# Mutually exclusive movement args
rotation = parser.add_mutually_exclusive_group()
rotation.add_argument('-n', '--num', type=int, default=None, help='Number of half steps to take. 4096 is a full rotation on a 28byj-48 motor')
rotation.add_argument('-d', '--degrees', type=float, default=None, help='Degrees to turn')
rotation.add_argument('-t', '--time', type=float, help='Seconds to rotate')

args = parser.parse_args()

# Replace this with the GPIO pins you plan to use
in1 = 14
in2 = 15
in3 = 24
in4 = 23

with StepperMotor(in1, in2, in3, in4) as motor:
    motor.load_exit_options('exitoptions.json')
    try:
        if args.num is not None:
            motor.take_steps(args.steps_per_sec, args.num, not args.reverse)
        elif args.degrees is not None:
            motor.turn_degrees(args.steps_per_sec, args.degrees, not args.reverse)
        elif args.time is not None:
            motor.turn_time(args.steps_per_sec, args.time, not args.reverse)
        else:
            motor.turn(args.steps_per_sec, not args.reverse)
    except KeyboardInterrupt:
        pass
    motor.write_exit_options('exitoptions.json')
