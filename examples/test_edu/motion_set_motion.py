from openpibo.pibo import Edu_Pibo


def motion_test():
    pibo = Edu_Pibo()
    ret=pibo.set_motion("dance1", 2)
    print(ret)

if __name__ == "__main__":
    motion_test()