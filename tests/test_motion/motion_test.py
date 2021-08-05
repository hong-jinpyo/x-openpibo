import os
import sys

# 상위 디렉토리 추가 (for utils.config)
sys.path.append('../..')
from utils.config import Config as cfg

# openpibo 라이브러리 경로 추가
sys.path.append(cfg.OPENPIBO_PATH + '/lib')
from motion import Motion

if __name__ == "__main__":
  m = Motion(conf=cfg)
  m.set_motion(name="wave3", cycle=10)
