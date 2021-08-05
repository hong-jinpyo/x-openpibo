import time

from openpibo.pibo import Edu_Pibo


def movetime_test():
    pibo = Edu_Pibo()
    while True:
        pibo.motors_movetime(positions=[0,0,30,20, 30,0, 0,0,30,20], movetime=1000)
        time.sleep(1)
        pibo.motors_movetime(positions=[0,0,-30,-20, -30,0, 0,0,-30,-20])
        time.sleep(1)

if __name__ == "__main__":
    movetime_test()