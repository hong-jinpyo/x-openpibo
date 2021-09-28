# from modules import move
# from modules import RPIservo


import time
import RPi.GPIO as GPIO

# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

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
    
    def motor_right(self, status, direction, speed):#Motor 1 positive and negative rotation
        """우측 모터를 제어합니다."""

        if status == 0: # stop
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            GPIO.output(Motor_A_EN, GPIO.LOW)
        else:
            if direction == forward:#
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

        #speed = 100
        if direction == 'forward':
            if turn == 'right':
                self.motor_left(0, backward, int(speed*radius))
                self.motor_right(1, forward, speed)
            elif turn == 'left':
                self.motor_left(1, forward, speed)
                self.motor_right(0, backward, int(speed*radius))
            else:
                self.motor_left(1, forward, speed)
                self.motor_right(1, forward, speed)
        elif direction == 'backward':
            if turn == 'right':
                self.motor_left(0, forward, int(speed*radius))
                self.motor_right(1, backward, speed)
            elif turn == 'left':
                self.motor_left(1, backward, speed)
                self.motor_right(0, forward, int(speed*radius))
            else:
                self.motor_left(1, backward, speed)
                self.motor_right(1, backward, speed)
        elif direction == 'no':
            if turn == 'right':
                self.motor_left(1, backward, speed)
                self.motor_right(1, forward, speed)
            elif turn == 'left':
                self.motor_left(1, forward, speed)
                self.motor_right(1, backward, speed)
            else:
                self.motorStop()
        else:
            pass
    
    def motorStop(self):#Motor stops
        """모터를 정지합니다."""

        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)

# if __name__ == "__main__":
    # speed_set = 60
    # picar_dc = DCMotor()
    # picar_dc.move(speed_set, 'forward', 'no', 0.8)
    # time.sleep(1.3)
    # picar_dc.motorStop()
    # GPIO.cleanup()


import Adafruit_PCA9685
import threading

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

init_pwm0 = 300
init_pwm1 = 300
init_pwm2 = 300
init_pwm3 = 300

init_pwm4 = 300
init_pwm5 = 300
init_pwm6 = 300
init_pwm7 = 300

init_pwm8 = 300
init_pwm9 = 300
init_pwm10 = 300
init_pwm11 = 300

init_pwm12 = 300
init_pwm13 = 300
init_pwm14 = 300
init_pwm15 = 300

class ServoMotor:
    """서보 모터를 제어합니다."""
    
    def __init__(self, *args, **kwargs):
        self.sc_direction = [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1]
        self.initPos = [init_pwm0,init_pwm1,init_pwm2,init_pwm3,
                        init_pwm4,init_pwm5,init_pwm6,init_pwm7,
                        init_pwm8,init_pwm9,init_pwm10,init_pwm11,
                        init_pwm12,init_pwm13,init_pwm14,init_pwm15]
        self.goalPos = [300,300,300,300, 300,300,300,300 ,300,300,300,300 ,300,300,300,300]
        self.nowPos  = [300,300,300,300, 300,300,300,300 ,300,300,300,300 ,300,300,300,300]
        self.bufferPos  = [300.0,300.0,300.0,300.0, 300.0,300.0,300.0,300.0 ,300.0,300.0,300.0,300.0 ,300.0,300.0,300.0,300.0]
        self.lastPos = [300,300,300,300, 300,300,300,300 ,300,300,300,300 ,300,300,300,300]
        self.ingGoal = [300,300,300,300, 300,300,300,300 ,300,300,300,300 ,300,300,300,300]
        self.maxPos  = [560,560,560,560, 560,560,560,560 ,560,560,560,560 ,560,560,560,560]
        self.minPos  = [100,100,100,100, 100,100,100,100 ,100,100,100,100 ,100,100,100,100]
        self.scSpeed = [0,0,0,0, 0,0,0,0 ,0,0,0,0 ,0,0,0,0]

        self.ctrlRangeMax = 560
        self.ctrlRangeMin = 100
        self.angleRange = 180

        '''
        scMode: 'init' 'auto' 'certain' 'quick' 'wiggle'
        '''
        self.scMode = 'auto'
        self.scTime = 2.0
        self.scSteps = 30
        
        self.scDelay = 0.037
        self.scMoveTime = 0.037

        self.goalUpdate = 0
        self.wiggleID = 0
        self.wiggleDirection = 1

        super(ServoMotor, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()


    def pause(self):
        print('......................pause..........................')
        self.__flag.clear()


    def resume(self):
        print('resume')
        self.__flag.set()


    def moveInit(self):
        self.scMode = 'init'
        for i in range(0,16):
            pwm.set_pwm(i,0,self.initPos[i])
            self.lastPos[i] = self.initPos[i]
            self.nowPos[i] = self.initPos[i]
            self.bufferPos[i] = float(self.initPos[i])
            self.goalPos[i] = self.initPos[i]
        self.pause()


    def initConfig(self, ID, initInput, moveTo):
        if initInput > self.minPos[ID] and initInput < self.maxPos[ID]:
            self.initPos[ID] = initInput
            if moveTo:
                pwm.set_pwm(ID,0,self.initPos[ID])
        else:
            print('initPos Value Error.')


    def moveServoInit(self, ID):
        self.scMode = 'init'
        for i in range(0,len(ID)):
            pwm.set_pwm(ID[i], 0, self.initPos[ID[i]])
            self.lastPos[ID[i]] = self.initPos[ID[i]]
            self.nowPos[ID[i]] = self.initPos[ID[i]]
            self.bufferPos[ID[i]] = float(self.initPos[ID[i]])
            self.goalPos[ID[i]] = self.initPos[ID[i]]
        self.pause()


    def posUpdate(self):
        self.goalUpdate = 1
        for i in range(0,16):
            self.lastPos[i] = self.nowPos[i]
        self.goalUpdate = 0


    def speedUpdate(self, IDinput, speedInput):
        for i in range(0,len(IDinput)):
            self.scSpeed[IDinput[i]] = speedInput[i]


    def moveAuto(self):
        for i in range(0,16):
            self.ingGoal[i] = self.goalPos[i]

        for i in range(0, self.scSteps):
            for dc in range(0,16):
                if not self.goalUpdate:
                    self.nowPos[dc] = int(round((self.lastPos[dc] + (((self.goalPos[dc] - self.lastPos[dc])/self.scSteps)*(i+1))),0))
                    pwm.set_pwm(dc, 0, self.nowPos[dc])

                if self.ingGoal != self.goalPos:
                    self.posUpdate()
                    time.sleep(self.scTime/self.scSteps)
                    return 1
            time.sleep((self.scTime/self.scSteps - self.scMoveTime))

        self.posUpdate()
        self.pause()
        return 0


    def moveCert(self):
        for i in range(0,16):
            self.ingGoal[i] = self.goalPos[i]
            self.bufferPos[i] = self.lastPos[i]

        while self.nowPos != self.goalPos:
            for i in range(0,16):
                if self.lastPos[i] < self.goalPos[i]:
                    self.bufferPos[i] += self.pwmGenOut(self.scSpeed[i])/(1/self.scDelay)
                    newNow = int(round(self.bufferPos[i], 0))
                    if newNow > self.goalPos[i]:newNow = self.goalPos[i]
                    self.nowPos[i] = newNow
                elif self.lastPos[i] > self.goalPos[i]:
                    self.bufferPos[i] -= self.pwmGenOut(self.scSpeed[i])/(1/self.scDelay)
                    newNow = int(round(self.bufferPos[i], 0))
                    if newNow < self.goalPos[i]:newNow = self.goalPos[i]
                    self.nowPos[i] = newNow

                if not self.goalUpdate:
                    pwm.set_pwm(i, 0, self.nowPos[i])

                if self.ingGoal != self.goalPos:
                    self.posUpdate()
                    return 1
            self.posUpdate()
            time.sleep(self.scDelay-self.scMoveTime)

        else:
            self.pause()
            return 0


    def pwmGenOut(self, angleInput):
        return int(round(((self.ctrlRangeMax-self.ctrlRangeMin)/self.angleRange*angleInput),0))


    def setAutoTime(self, autoSpeedSet):
        self.scTime = autoSpeedSet


    def setDelay(self, delaySet):
        self.scDelay = delaySet


    def autoSpeed(self, ID, angleInput):
        self.scMode = 'auto'
        self.goalUpdate = 1
        for i in range(0,len(ID)):
            newGoal = self.initPos[ID[i]] + self.pwmGenOut(angleInput[i])*self.sc_direction[ID[i]]
            if newGoal>self.maxPos[ID[i]]:newGoal=self.maxPos[ID[i]]
            elif newGoal<self.minPos[ID[i]]:newGoal=self.minPos[ID[i]]
            self.goalPos[ID[i]] = newGoal
        self.goalUpdate = 0
        self.resume()


    def certSpeed(self, ID, angleInput, speedSet):
        self.scMode = 'certain'
        self.goalUpdate = 1
        for i in range(0,len(ID)):
            newGoal = self.initPos[ID[i]] + self.pwmGenOut(angleInput[i])*self.sc_direction[ID[i]]
            if newGoal>self.maxPos[ID[i]]:newGoal=self.maxPos[ID[i]]
            elif newGoal<self.minPos[ID[i]]:newGoal=self.minPos[ID[i]]
            self.goalPos[ID[i]] = newGoal
        self.speedUpdate(ID, speedSet)
        self.goalUpdate = 0
        self.resume()


    def moveWiggle(self):
        self.bufferPos[self.wiggleID] += self.wiggleDirection*self.sc_direction[self.wiggleID]*self.pwmGenOut(self.scSpeed[self.wiggleID])/(1/self.scDelay)
        newNow = int(round(self.bufferPos[self.wiggleID], 0))
        if self.bufferPos[self.wiggleID] > self.maxPos[self.wiggleID]:self.bufferPos[self.wiggleID] = self.maxPos[self.wiggleID]
        elif self.bufferPos[self.wiggleID] < self.minPos[self.wiggleID]:self.bufferPos[self.wiggleID] = self.minPos[self.wiggleID]
        self.nowPos[self.wiggleID] = newNow
        self.lastPos[self.wiggleID] = newNow
        if self.bufferPos[self.wiggleID] < self.maxPos[self.wiggleID] and self.bufferPos[self.wiggleID] > self.minPos[self.wiggleID]:
            pwm.set_pwm(self.wiggleID, 0, self.nowPos[self.wiggleID])
        else:
            self.stopWiggle()
        time.sleep(self.scDelay-self.scMoveTime)


    def stopWiggle(self):
        self.pause()
        self.posUpdate()


    def singleServo(self, ID, direcInput, speedSet):
        self.wiggleID = ID
        self.wiggleDirection = direcInput
        self.scSpeed[ID] = speedSet
        self.scMode = 'wiggle'
        self.posUpdate()
        self.resume()


    def moveAngle(self, ID, angleInput):
        self.nowPos[ID] = int(self.initPos[ID] + self.sc_direction[ID]*self.pwmGenOut(angleInput))
        if self.nowPos[ID] > self.maxPos[ID]:self.nowPos[ID] = self.maxPos[ID]
        elif self.nowPos[ID] < self.minPos[ID]:self.nowPos[ID] = self.minPos[ID]
        self.lastPos[ID] = self.nowPos[ID]
        pwm.set_pwm(ID, 0, self.nowPos[ID])


    def scMove(self):
        if self.scMode == 'init':
            self.moveInit()
        elif self.scMode == 'auto':
            self.moveAuto()
        elif self.scMode == 'certain':
            self.moveCert()
        elif self.scMode == 'wiggle':
            self.moveWiggle()


    def setPWM(self, ID, PWM_input):
        self.lastPos[ID] = PWM_input
        self.nowPos[ID] = PWM_input
        self.bufferPos[ID] = float(PWM_input)
        self.goalPos[ID] = PWM_input
        pwm.set_pwm(ID, 0, PWM_input)
        self.pause()


    def run(self):
        while 1:
            self.__flag.wait()
            self.scMove()
            pass


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
    
    def run(self):
        self.status_right = GPIO.input(line_pin_right)
        self.status_middle = GPIO.input(line_pin_middle)
        self.status_left = GPIO.input(line_pin_left)
        return (self.status_left, self.status_middle, self.status_right)
    

class Camera:
    """카메라를 제어합니다."""
    pass




class Driving:
    """DC 모터와 방향 서보모터를 컨트롤한다."""

    # move.setup()

    def __init__(self):
        self.scGear = RPIservo.ServoCtrl()
        self.scGear.moveInit()
        self.move = move.move
        self.speed = 60
        pass

    def drive(self, moveAngle, direction='forward', turn='no', radius=0.8):
        self.move(self.speed, direction, turn, radius)
        self.scGear.moveAngle(0, moveAngle)
    
    def stop(self):
        move.motorStop()
    
    def setSpeed(self, speed):
        self.speed = speed


# class Tracking:
#     """검정색 선을 추적한다."""

#     left_forward  = 1
#     left_backward = 0

#     right_forward = 0
#     right_backward= 1
#     # timestart = time.time()
#     mark = 0

#     def __init__(self):
#         self.line_pin_right = 20
#         self.line_pin_middle = 16
#         self.line_pin_left = 19
#         # GPIO.setwarnings(False)
#         # GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.line_pin_right,GPIO.IN)
#         GPIO.setup(self.line_pin_middle,GPIO.IN)
#         GPIO.setup(self.line_pin_left,GPIO.IN)
#         self.status = (None, None, None)
    
#     def check(self):
#         status_right = GPIO.input(self.line_pin_right)
#         status_middle = GPIO.input(self.line_pin_middle)
#         status_left = GPIO.input(self.line_pin_left)
#         self.status = (status_left, status_middle, status_right)
#         return self.status


# from modules.camera_opencv import Camera
# from importlib import import_module
# import os
# from flask import Flask, render_template, Response
# import threading
# from modules.camera_opencv import CVThread
class Vision:
    """카메라로 타겟 색깔의 위치(중앙 포인트)를 가져온다."""

    def __init__(self):
        self.camera = Camera()
        self.CVThreading = 0
        self.CVThread = CVThread()

    def findColor(self):
        frame = self.camera.get_frame()
        self.camera.modeSet('findColor')
        color = self.camera.frames()

    def gen(camera):
        """Video streaming generator function."""
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    def findlineCV(self):
        print(self.camera.frames())
    
    # def web_view(self):


# if __name__ == '__main__':
    # picar = Driving()
    # try:
    #     while True:
    #         picar.drive(60)
    # except Exception as e:
    #     print(e)

    # picar = Tracking()
    # while True:
    #     print(picar.check())
    #     time.sleep(1)