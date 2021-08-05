import time
from openpibo.pibo import Edu_Pibo

def streaming_test():
    pibo = Edu_Pibo()

    pibo.start_camera()
    time.sleep(3)
    pibo.stop_camera()
    
if __name__ == "__main__":
    streaming_test()