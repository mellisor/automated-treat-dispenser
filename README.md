# Automated Treat Dispenser Project

## Project Description

This repo contains the bits of code that power the treat dispenser you can find at {insert URL here}. All you should need to do is install the `gpiod` package, update the code, then run the command `python motor.py 512 -d 45` to rotate the divider by one segment

## Installing the necessary packages

This repo uses pipenv for package management, not that it's complicated enough to need it. If you don't have pipenv installed already, you can install it with `sudo apt install pipenv`. After it is installed, you should be able to run `pipenv shell` then `pipenv install`.

## Updating the code

The script that powers the motor is written in python. There's not much that should need to be changed here aside from the four variables that represent the GPIO pins that will be hooked up to the inputs of the motor driver. Make sure in1, in2, in3, and in4 are updated to correspond to the pin connected to each input on the board.
