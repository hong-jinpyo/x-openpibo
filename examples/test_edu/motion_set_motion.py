import os, sys, time

sys.path.append('../..')
from utils.config import Config as cfg

sys.path.append(cfg.OPENPIBO_PATH + '/lib/edu')
from pibo import Edu_Pibo


def motion_test():
    pibo = Edu_Pibo()
    ret=pibo.set_motion("dance1", 2)
    print(ret)

if __name__ == "__main__":
    motion_test()