import RPi.GPIO as GPIO
from time import sleep
import pigpio


class Servo:
    angle_0 = 500
    angle_90 = 1500
    angle_180 = 2500
    pulsewidth_range = 2000

    def __init__(self, Pin, init_angle):
        self.pin = Pin
        self.servo = pigpio.pi()
        self.set_angle(init_angle)

    def set_angle(self, angle):
        self.current_angle = angle
        pulsewidth = 500+self.current_angle*Servo.pulsewidth_range/180
        self.servo.set_servo_pulsewidth(self.pin, pulsewidth)
        sleep(1)
        self.servo.set_PWM_dutycycle(self.pin, 0)

    def turn_clockwise(self, step_angle):
        # clockwise
        angle = self.current_angle-step_angle
        if angle < 0:
            angle = 0
        self.set_angle(angle)

    def turn_anti_clockwise(self, step_angle):
        # anti_clockwise
        angle = self.current_angle+step_angle
        if angle > 180:
            angle = 180
        self.set_angle(angle)

    def __exit__(self, exc_type, exc_value, traceback):
        self.servo.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    vertical_servo = Servo(18, 90)
    sleep(1)
    vertical_servo.turn_clockwise(20)
    sleep(1)
    vertical_servo.turn_anti_clockwise(20)
    sleep(1)
    vertical_servo.set_angle(90)
    sleep(1)
    #
    horizontal_servo = Servo(19, 90)
    horizontal_servo.turn_clockwise(20)
    sleep(1)
    horizontal_servo.turn_anti_clockwise(20)
    sleep(1)
    horizontal_servo.set_angle(90)
    sleep(1)
