import time
from openpibo.pibo import Edu_Pibo

def text_test():
    pibo = Edu_Pibo()

    ret = pibo.draw_text((10,10), '안녕하세요. Hello', 15)
    print(ret)
    pibo.show_display()
    time.sleep(2)
    pibo.clear_display()

if __name__ == "__main__":
    text_test()