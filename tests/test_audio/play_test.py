import time
import sys

# 상위 디렉토리 추가 (for utils.config)
sys.path.append("../../utils")
from config import Config as cfg

# openpibo 라이브러리 경로 추가
sys.path.append(cfg.OPENPIBO_PATH)
from openpibo.audio import Audio

def tts_f():
  obj = Audio()
  obj.play(filename=cfg.MP3_TESTDATA_PATH+"/test.mp3", out='local', volume=-2000)
  time.sleep(5)
  obj.stop()

if __name__ == "__main__":
  tts_f()
