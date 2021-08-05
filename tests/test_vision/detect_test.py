import os
import sys

# 상위 디렉토리 추가 (for utils.config)
sys.path.append('../..')
from utils.config import Config as cfg

# openpibo 라이브러리 경로 추가
sys.path.append(cfg.OPENPIBO_PATH + '/lib')
from vision import Camera
from vision import Detect

def test_func():
  # instance
  cam = Camera()
  det = Detect(conf=cfg)

  # Capture / Read file
  img = cam.read()
  #img = cam.imread("image.jpg")

  print("Object Detect: ", det.detect_object(img))
  print("Qr Detect:", det.detect_qr(img))
  print("Text Detect:", det.detect_text(img))

if __name__ == "__main__":
  test_func()
