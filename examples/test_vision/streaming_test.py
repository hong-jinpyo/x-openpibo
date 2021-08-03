import os
import sys

# 상위 디렉토리 추가 (for utils.config)
sys.path.append('../..')
from utils.config import Config as cfg

# openpibo 라이브러리 경로 추가
sys.path.append(cfg.OPENPIBO_PATH + '/lib')
from vision import cCamera

def test_func():
  # instance
  cam = cCamera()

  # For streaming (only GUI)
  cam.streaming(timeout=3)

if __name__ == "__main__":
  test_func()
