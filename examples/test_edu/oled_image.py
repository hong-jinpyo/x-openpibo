import time
import openpibo
from openpibo.pibo import Edu_Pibo

def image_test():
    pibo = Edu_Pibo()

    ret=pibo.draw_image(openpibo.data_path+"images/clear.png")
    print(ret)
    pibo.show_display()
    time.sleep(2)
    pibo.clear_display()

if __name__ == "__main__":
    image_test()