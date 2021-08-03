import os, sys, time

sys.path.append('../..')
from utils.config import Config as cfg

sys.path.append(cfg.OPENPIBO_PATH + '/lib/edu')
from pibo import Edu_Pibo

def image_test():
    pibo = Edu_Pibo()

    ret=pibo.draw_image(cfg.IMAGES_TESTDATA_PATH +"/clear.png")
    print(ret)
    pibo.show_display()
    time.sleep(2)
    pibo.clear_display()

if __name__ == "__main__":
    image_test()