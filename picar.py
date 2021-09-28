from openpibo.picar_lib import DCMotor, ServoMotor, Tracking
import time

dcmotor = DCMotor()
servomotor = ServoMotor()
tracking = Tracking()
mark = 0

while True:
    state = tracking.run()
    print(state)
    speed = 60
    dcmotor.move(speed, 'forward', 'no')
    if state == (0, 1, 0):
        servomotor.moveAngle(0, 0)
        mark = 1
    elif state == (1, 1, 0):
        servomotor.moveAngle(0, 15)
        mark = 2
    elif state == (1, 0, 0):
        servomotor.moveAngle(0, 30)
        mark = 3
    elif state == (0, 1, 1):
        servomotor.moveAngle(0, -15)
        mark = 4
    elif state == (0, 0, 1):
        servomotor.moveAngle(0, -30)
        mark = 5
    else:
        if mark == 0 or mark == 1:
            servomotor.moveAngle(0, 0)
        elif mark == 2 or mark == 3:
            servomotor.moveAngle(0, 60)
        elif mark == 4 or mark == 5:
            servomotor.moveAngle(0, -60)
    time.sleep(0.1)