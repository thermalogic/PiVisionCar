import RPi.GPIO as GPIO
from time import sleep

from .servo_pigpio import Servo


class Dual_Axis:
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    def __init__(self, Vertical_Pin, Vertical_init_angle, horizontal_Pin, horizontal_init_angle):
        self.vertical_servo = Servo(Vertical_Pin, Vertical_init_angle)
        self.horizontal_servo = Servo(horizontal_Pin, horizontal_init_angle)

        self.DICT_CMD_ACTION = {Dual_Axis.LEFT: self.turn_left,
                                Dual_Axis.RIGHT: self.turn_right,
                                Dual_Axis.UP: self.turn_up,
                                Dual_Axis.DOWN: self.turn_down
                                }
        self.each_step_angle = 5

    def turn_left(self):
        self.vertical_servo.turn_clockwise(self.each_step_angle)

    def turn_right(self):
        self.vertical_servo.turn_anti_clockwise(self.each_step_angle)

    def turn_up(self):
        self.horizontal_servo.turn_anti_clockwise(self.each_step_angle)

    def turn_down(self):
        self.horizontal_servo.turn_clockwise(self.each_step_angle)

    def action(self, cmd_to_dual_axis):
        self.DICT_CMD_ACTION[cmd_to_dual_axis]()
