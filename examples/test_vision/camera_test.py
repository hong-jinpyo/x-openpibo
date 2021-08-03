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

  # Capture / Read file
  img = cam.read()
  #img = cam.imread("/home/pi/test.jpg")

  # Write
  cam.imwrite("test.jpg", img)

  # display (only GUI)
  cam.imshow(img, "TITLE")
  cam.waitKey(3000)

if __name__ == "__main__":
  test_func()
