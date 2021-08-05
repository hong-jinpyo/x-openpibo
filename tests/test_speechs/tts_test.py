import os
import sys

# 상위 디렉토리 추가 (for utils.config)
sys.path.append('../..')
from utils.config import Config as cfg

# openpibo 라이브러리 경로 추가
sys.path.append(cfg.OPENPIBO_PATH + '/lib')
from speech import Speech
from audio import Audio

def tts_f():
  tObj = Speech(conf=cfg)
  filename = cfg.MP3_TESTDATA_PATH+"/tts.mp3"
  tObj.tts("<speak>\
              <voice name='MAN_READ_CALM'>안녕하세요. 반갑습니다.<break time='500ms'/></voice>\
            </speak>"\
          , filename)
  print(filename)
  aObj = Audio()
  aObj.play(filename, out='local', volume=-1500)

if __name__ == "__main__":
  tts_f()
