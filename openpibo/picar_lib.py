"""
DCMotor
=======
"""

import time
import RPi.GPIO as GPIO

Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 26
Motor_A_Pin2  = 21
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

forward   = 0
backward  = 1

pwm_A = 0
pwm_B = 0

class DCMotor:
    """DC 모터를 제어합니다."""
    
    def __init__(self):
        """DC 모터 GPIO를 연결하고 초기화합니다."""

        global pwm_A, pwm_B
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Motor_A_EN, GPIO.OUT)
        GPIO.setup(Motor_B_EN, GPIO.OUT)
        GPIO.setup(Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(Motor_B_Pin2, GPIO.OUT)

        self.motorStop()
        try:
            pwm_A = GPIO.PWM(Motor_A_EN, 1000)
            pwm_B = GPIO.PWM(Motor_B_EN, 1000)
        except:
            pass
    
    def motor_right(self, status, direction, speed):
        """우측 모터를 제어합니다."""

        if status == 0: # stop
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            GPIO.output(Motor_A_EN, GPIO.LOW)
        else:
            if direction == forward:
                GPIO.output(Motor_A_Pin1, GPIO.LOW)
                GPIO.output(Motor_A_Pin2, GPIO.HIGH)
                pwm_A.start(0)
                pwm_A.ChangeDutyCycle(speed)
            elif direction == backward:
                GPIO.output(Motor_A_Pin1, GPIO.HIGH)
                GPIO.output(Motor_A_Pin2, GPIO.LOW)
                pwm_A.start(100)
                pwm_A.ChangeDutyCycle(speed)
    
    def motor_left(self, status, direction, speed):
        """좌측 모터를 제어합니다."""

        if status == 0: # stop
            GPIO.output(Motor_B_Pin1, GPIO.LOW)
            GPIO.output(Motor_B_Pin2, GPIO.LOW)
            GPIO.output(Motor_B_EN, GPIO.LOW)
        else:
            if direction == forward:
                GPIO.output(Motor_B_Pin1, GPIO.LOW)
                GPIO.output(Motor_B_Pin2, GPIO.HIGH)
                pwm_B.start(0)
                pwm_B.ChangeDutyCycle(speed)
            elif direction == backward:
                GPIO.output(Motor_B_Pin1, GPIO.HIGH)
                GPIO.output(Motor_B_Pin2, GPIO.LOW)
                pwm_B.start(100)
                pwm_B.ChangeDutyCycle(speed)
    
    def move(self, speed, direction, turn, radius=0.8):   # 0 < radius <= 1  
        """양쪽 모터를 제어하여 기기를 움직입니다."""

        if direction == 'forward':
            self.motor_left(1, forward, speed - (turn * radius))
            self.motor_right(1, forward, speed + (turn * radius))

        elif direction == 'backward':
            self.motor_left(1, backward, speed - (turn * radius))
            self.motor_right(1, backward, speed + (turn * radius))

        else:
            pass
    
    def motorStop(self):
        """모터를 정지합니다."""

        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)


"""
ServoMotor
==========
"""

import Adafruit_PCA9685
import threading

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

init_pwm0 = 300
init_pwm1 = 300
init_pwm2 = 300

class ServoMotor:
    """
    서보 모터를 제어합니다.
    기존 16개 서보모터 -> 3개로 축소
    0: 앞바퀴 방향. 0=정면
    1: 카메라 좌우. 0=정면
    2: 카메라 상하. 0=정면
    """
    
    def __init__(self):
        self.sc_direction = [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1]
        self.initPos = [init_pwm0,init_pwm1,init_pwm2]
        self.nowPos  = [300,300,300]
        self.maxPos  = [560,560,560]
        self.minPos  = [100,100,100]

        self.ctrlRangeMax = 560
        self.ctrlRangeMin = 100
        self.angleRange = 180

        self.initConfig(1, 297, 1)
        self.initConfig(2, 140, 1)

    def moveInit(self):
        for i in range(0,3):
            pwm.set_pwm(i,0,self.initPos[i])
            self.nowPos[i] = self.initPos[i]


    def initConfig(self, ID, initInput, moveTo):
        if initInput > self.minPos[ID] and initInput < self.maxPos[ID]:
            self.initPos[ID] = initInput
            if moveTo:
                pwm.set_pwm(ID,0,self.initPos[ID])
        else:
            print('initPos Value Error.')


    def moveServoInit(self, ID):
        for i in range(0,len(ID)):
            pwm.set_pwm(ID[i], 0, self.initPos[ID[i]])
            self.nowPos[ID[i]] = self.initPos[ID[i]]


    def pwmGenOut(self, angleInput):
        return int(round(((self.ctrlRangeMax-self.ctrlRangeMin)/self.angleRange*angleInput),0))


    def moveAngle(self, ID, angleInput):
        self.nowPos[ID] = int(self.initPos[ID] + self.sc_direction[ID]*self.pwmGenOut(angleInput))
        if self.nowPos[ID] > self.maxPos[ID]:self.nowPos[ID] = self.maxPos[ID]
        elif self.nowPos[ID] < self.minPos[ID]:self.nowPos[ID] = self.minPos[ID]
        pwm.set_pwm(ID, 0, self.nowPos[ID])


    def setPWM(self, ID, PWM_input):
        self.nowPos[ID] = PWM_input
        pwm.set_pwm(ID, 0, PWM_input)


"""
Tracking
========
"""

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

class Tracking:
    """트래킹 모듈을 제어합니다."""

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(line_pin_right,GPIO.IN)
        GPIO.setup(line_pin_middle,GPIO.IN)
        GPIO.setup(line_pin_left,GPIO.IN)
        self.status_right = None
        self.status_middle = None
        self.status_left = None
    
    def get_signal(self):
        self.status_right = GPIO.input(line_pin_right)
        self.status_middle = GPIO.input(line_pin_middle)
        self.status_left = GPIO.input(line_pin_left)
        return (self.status_left, self.status_middle, self.status_right)


"""
Camera
======
"""

import cv2
import numpy as np

def get_line(lineIndex_Pos, thickness, offset):
    lines = []
    left = 999
    right = 0
    for pixel in lineIndex_Pos[0]:
        if pixel != right + 1:
            if abs((right - left) - thickness) <= offset:
                line_center = (left + right) // 2
                lines.append(line_center)
                left = pixel
                continue
            left = pixel
        pixel_old = pixel
        right = pixel
    lines.sort(key=lambda x: abs(x - 320))
    return lines[0]

class Camera:
    """카메라를 제어합니다."""

    def __init__(self):
        self.linePos_1 = 440
        self.linePos_2 = 380
        self.lineColorSet = 0

        self.center_Pos1 = None

        self.center_Pos2 = None
    
        self.center = None

        self.thickness1 = 88
        self.thickness2 = 78
        self.offset = 20

        self.camera = cv2.VideoCapture(0)
    
    def set_thick(self, thickness, offset):
        self.thickness1 = thickness
        self.thickness2 = int(thickness * 0.9)
        self.offset = offset

    def findline(self):
        _, frame_image = self.camera.read()
        frame_findline = cv2.cvtColor(frame_image, cv2.COLOR_BGR2GRAY)
        retval, frame_findline =  cv2.threshold(frame_findline, 0, 255, cv2.THRESH_OTSU)
        frame_findline = cv2.erode(frame_findline, None, iterations=6)
        colorPos_1 = frame_findline[self.linePos_1]
        colorPos_2 = frame_findline[self.linePos_2]
        try:
            lineIndex_Pos1 = np.where(colorPos_1 == self.lineColorSet)
            lineIndex_Pos2 = np.where(colorPos_2 == self.lineColorSet)

            self.center_Pos1 = get_line(lineIndex_Pos1, self.thickness1, self.offset)
            self.center_Pos2 = get_line(lineIndex_Pos2, self.thickness2, self.offset)

            self.center = (self.center_Pos1 + self.center_Pos2) // 2

        except:
            self.center = 320

        return self.center
