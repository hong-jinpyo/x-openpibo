import os, sys, time

sys.path.append('../..')
from utils.config import Config as cfg

sys.path.append(cfg.OPENPIBO_PATH + '/lib/edu')
from pibo import Edu_Pibo

def audio_test():
    pibo = Edu_Pibo()
    ret=pibo.play_audio(filename=cfg.MP3_TESTDATA_PATH+"/test.mp3", out='local', volume=-2000)
    print(ret)
    time.sleep(3)
    pibo.stop_audio()

if __name__ == "__main__":
    audio_test()