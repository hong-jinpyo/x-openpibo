from openpibo.picar_lib import DCMotor, ServoMotor, Camera
import time

dcmotor = DCMotor()

servomotor = ServoMotor()
servomotor.moveAngle(2,-40)

camera = Camera()
camera.set_thick(88, 20)

mark = 0

while True:
    target = camera.findline()
    print(target)
    speed = 60
    dcmotor.move(speed, 'forward', 0)
    direction = ((320 - target) * 60) // 320
    servomotor.moveAngle(0, direction)
    time.sleep(0.1)