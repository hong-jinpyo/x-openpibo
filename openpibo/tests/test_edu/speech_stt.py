import os, sys, time

sys.path.append('../..')
from utils.config import Config as cfg

sys.path.append(cfg.OPENPIBO_PATH + '/lib/edu')
from pibo import Edu_Pibo

def stt_test():
    pibo = Edu_Pibo()

    ret = pibo.stt()
    print(ret)

if __name__ == "__main__":
    stt_test()