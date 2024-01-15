import gpiod
from gpiod.line import Direction, Value
import time
import datetime
import json
import math

ON = Value.ACTIVE
OFF = Value.INACTIVE

step_outputs = [
 [ON, OFF, OFF, OFF],
 [ON, ON, OFF, OFF],
 [OFF, ON, OFF, OFF],
 [OFF, ON, ON, OFF],
 [OFF, OFF, ON, OFF],
 [OFF, OFF, ON, ON],
 [OFF, OFF, OFF, ON],
 [ON, OFF, OFF, ON],
]

class StepperMotor(object):

    in1: int
    in2: int
    in3: int
    in4: int

    current_step: int
    steps_per_rotation: int

    gpio: gpiod.LineRequest

    def __init__(self, in1: int, in2: int, in3: int, in4: int):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        self.steps_per_rotation = 4096 # Actually 2048, but half steps work better when powering the motor off the pi's 5V pin
        self.current_step = 0

    def __enter__(self):
        self.gpio = gpiod.request_lines(
            "/dev/gpiochip0",
            consumer="motor-test",
            config={
                self.in1: gpiod.LineSettings(direction = Direction.OUTPUT, output_value = OFF),
                self.in2: gpiod.LineSettings(direction = Direction.OUTPUT, output_value = OFF),
                self.in3: gpiod.LineSettings(direction = Direction.OUTPUT, output_value = OFF),
                self.in4: gpiod.LineSettings(direction = Direction.OUTPUT, output_value = OFF)
            })
        return self
        
    def __exit__(self, *args):
        # After a small delay, ensure the motor is pointing at the current step
        time.sleep(.01)
        outputs = step_outputs[self.current_step]
        self.gpio.set_values({
            self.in1: outputs[0],
            self.in2: outputs[1],
            self.in3: outputs[2],
            self.in4: outputs[3]
        })

        # After another small delay, disable all pins
        time.sleep(.01)
        self.gpio.set_values({
            self.in1: OFF,
            self.in2: OFF,
            self.in3: OFF,
            self.in4: OFF
        })
        time.sleep(.01)
        self.gpio.__exit__(*args)

    def turn_degrees(self, steps_per_second: float, degrees: float, forward: bool = True):
        rotations = degrees / 360
        steps = int(rotations * self.steps_per_rotation)
        self.take_steps(steps_per_second, steps, forward)

    def take_steps(self, steps_per_second: float, steps: int, forward: bool = True):
        # When the motor has a load, adding a small acceleration period helps to ensure it doesn't slip
        # Start with a sleep time of .02 (50 steps per second)
        sleep_time = 1 / steps_per_second / 2
        actual_sleep_time = .02

        while steps > 0:
            steps -= 1

            # Advance to the next step in our list of inputs
            # Move backwards if we are going in reverse
            if forward:
                self.current_step += 1
            else:
                self.current_step -= 1

            # Ensure we are still in the bounds of our array
            self.current_step %= len(step_outputs)

            # Get our desired outputs and update the pins
            outputs = step_outputs[self.current_step]
            self.gpio.set_values({
                self.in1: outputs[0],
                self.in2: outputs[1],
                self.in3: outputs[2],
                self.in4: outputs[3]
            })

            # Sleep then accelerate by 10% if we haven't reached full speed
            time.sleep(actual_sleep_time)
            if actual_sleep_time > sleep_time:
                actual_sleep_time = max(sleep_time, actual_sleep_time / 1.1)

    def turn(self, steps_per_second: float, forward: bool = True):
        sleep_time = 1 / steps_per_second / 2
        while True:
            if forward:
                self.current_step += 1
            else:
                self.current_step -= 1

            self.current_step %= len(step_outputs)

            outputs = step_outputs[self.current_step]
            self.gpio.set_values({
                self.in1: outputs[0],
                self.in2: outputs[1],
                self.in3: outputs[2],
                self.in4: outputs[3]
            })
            time.sleep(sleep_time)

    def turn_time(self, steps_per_second: float, time: float, forward: bool = True):
        start = datetime.datetime.now()
        while True:
            elapsed = datetime.datetime.now() - start
            if (elapsed.seconds >= time):
                break

            self.take_steps(steps_per_second, 1, forward)

    def load_exit_options(self, file: str):
        try:
            with open(file) as f:
                # This is mainly useful when the previous execution ended on the non-default step.
                # Ex: Previously moved 3 steps. Running this again would start back at step 0 and the motor may not rotate until it catches up
                # There used to be more info on this object, but it wasn't necessary for this project so I removed it
                exit_options = json.load(f)
                self.current_step = exit_options['step']
        except:
            pass

    def write_exit_options(self, file: str):
        with open(file, 'w+') as f:
            json.dump({
                'step': self.current_step
            }, f)



        
