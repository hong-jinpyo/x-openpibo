import os, sys, time

sys.path.append('../..')
from utils.config import Config as cfg

sys.path.append(cfg.OPENPIBO_PATH + '/lib/edu')
from pibo import Edu_Pibo

def tts_test():
    pibo = Edu_Pibo()

    filename = cfg.MP3_TESTDATA_PATH+"/tts.mp3"
    ret=pibo.tts("<speak><voice name='WOMAN_READ_CALM'>안녕. 나는 파이보야.<break time='500ms'/></voice></speak>", filename)
    print(ret)
    pibo.play_audio(filename, out='local', volume=-1500)
    time.sleep(2)
    
if __name__ == "__main__":
    tts_test()