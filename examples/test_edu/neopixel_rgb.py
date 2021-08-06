import time
from openpibo.pibo import Edu_Pibo

def rgb_test():
    pibo = Edu_Pibo()
    ret = pibo.eye_on(0,255,0)
    print(ret)
    time.sleep(1.5)

    ret2 = pibo.eye_on(0,0,255,255,0,0)
    print(ret2)
    time.sleep(1.5)

    pibo.eye_off()

if __name__ == "__main__":
    rgb_test()