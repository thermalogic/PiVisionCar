import RPi.GPIO as GPIO
from time import sleep

class Motor:

    FORWARD = 0
    BACK = 1
    STOP = 2
    LEFT = 3
    RIGHT = 4

    SPEED_100=100
    SPEED_75=75
    SPEED_50=50
    SPEED_25=25
    

    def __init__(self,AIN1,AIN2,BIN1,BIN2):
        self.AIN1 = AIN1      
        self.AIN2 = AIN2     # right motor back - black GPIO 24 PCM_CLK 
        
        self.BIN1 = BIN1     # left red GPIO 25 PCM_CLK 
        self.BIN2 = BIN2     # left black GPIO 25 PCM_CLK 
        
        self.MOTOR_STATE = Motor.STOP

        self.speed= Motor.SPEED_75 # default speed 
        self.turn_diff_speed_percent=90  

        # init speed PWM
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        
        self.Right_Motor_Forward=GPIO.PWM(self.AIN1, 100)
        self.Right_Motor_Forward.start(0)
        self.Right_Motor_Back=GPIO.PWM(self.AIN2, 100)
        self.Right_Motor_Back.start(0)
     
        self.Left_Motor_Forward=GPIO.PWM(self.BIN1, 100)
        self.Left_Motor_Forward.start(0)
        self.Left_Motor_Back=GPIO.PWM(self.BIN2, 100)
        self.Left_Motor_Back.start(0)
      
        
        self.DICT_CMD_ACTION = {Motor.FORWARD: self.forward,
                                Motor.BACK: self.back,
                                Motor.STOP: self.stop,
                                Motor.LEFT: self.turn_left,
                                Motor.RIGHT: self.turn_right
                                }

    def forward(self):
        GPIO.output(self.AIN1, True)
        GPIO.output(self.AIN2, True)
        self.Right_Motor_Forward.ChangeDutyCycle(self.speed)
        self.Right_Motor_Back.ChangeDutyCycle(0)
        #GPIO.output(self.AIN1, GPIO.HIGH)
        #GPIO.output(self.AIN2, GPIO.LOW)
        # 
        self.Left_Motor_Forward.ChangeDutyCycle(self.speed)
        self.Left_Motor_Back.ChangeDutyCycle(0)
        GPIO.output(self.BIN1, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.LOW)


    def back(self):
        self.Right_Motor_Forward.ChangeDutyCycle(0)
        self.Right_Motor_Back.ChangeDutyCycle(self.speed)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.HIGH)
        # 
        self.Left_Motor_Forward.ChangeDutyCycle(0)
        self.Left_Motor_Back.ChangeDutyCycle(self.speed)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.HIGH)

    def stop(self):
        self.Right_Motor_Forward.ChangeDutyCycle(0)
        self.Right_Motor_Back.ChangeDutyCycle(0)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.LOW)
        # 
        self.Left_Motor_Forward.ChangeDutyCycle(0)
        self.Left_Motor_Back.ChangeDutyCycle(0)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)


    def turn_left(self):
        cur_speed=self.speed-int(self.turn_diff_speed_percent*self.speed/100)
        self.Right_Motor_Forward.ChangeDutyCycle(cur_speed)
        self.Right_Motor_Back.ChangeDutyCycle(0)
        GPIO.output(self.AIN1, True)
        GPIO.output(self.AIN2, True)
        # 
        self.Left_Motor_Forward.ChangeDutyCycle(self.speed)
        self.Left_Motor_Back.ChangeDutyCycle(0)
        GPIO.output(self.BIN2, True)
        GPIO.output(self.BIN2, True)


    def turn_right(self):
        self.Right_Motor_Forward.ChangeDutyCycle(self.speed)
        self.Right_Motor_Back.ChangeDutyCycle(0)
        GPIO.output(self.AIN1, True)
        GPIO.output(self.AIN2, True)
        # 
        cur_speed=self.speed-int(self.turn_diff_speed_percent*self.speed/100)
        self.Left_Motor_Forward.ChangeDutyCycle(cur_speed)
        self.Left_Motor_Back.ChangeDutyCycle(0)
        GPIO.output(self.BIN2, True)
        GPIO.output(self.BIN2, True)

    def action(self, cmd_to_motor):
        if (cmd_to_motor != self.MOTOR_STATE):
            self.MOTOR_STATE = cmd_to_motor
            self.DICT_CMD_ACTION[cmd_to_motor]()
    
    def adjust_speed(self,set_speed):
        # 前进后退速度
        if (self.speed!=set_speed):
            self.speed=set_speed
            self.DICT_CMD_ACTION[self.MOTOR_STATE]()

    def adjust_turn_speed(self,set_turn_speed):
        # 转向速度 -控制2侧速度差
        if (self.turn_speed!=set_turn_speed):
            self.turn_speed=set_turn_speed
            if (self.MOTOR_STATE== Motor.LEFT):
               self.turn_left()
            elif (self.MOTOR_STATE== Motor.RIGHT): 
               self.turn_right()
     
    def __exit__(self, exc_type, exc_value, traceback):
       self.Right_Motor_Forward.stop()
       self.Right_Motor_Back.stop()
       self.Left_Motor_Forward.stop()
       self.Left_Motor_Back.stop()
       GPIO.cleanup()           

if  __name__=="__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    car_motor=Motor(29,31,13,11)
    car_motor.forward()
    sleep(2)
    car_motor.stop()
    sleep(2)
    car_motor.back()
    sleep(2)
    car_motor.stop()
    sleep(2)
    car_motor.turn_left()
    sleep(2)
    car_motor.stop()
    sleep(2)
    car_motor.turn_right()
    sleep(2)
    car_motor.stop()
     
