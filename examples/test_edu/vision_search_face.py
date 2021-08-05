import time
from openpibo.pibo import Edu_Pibo

def face_test():
    pibo = Edu_Pibo()

    pibo.start_camera()
    time.sleep(3)
    face = pibo.search_face()
    print(face)
    pibo.stop_camera()
    
if __name__ == "__main__":
    face_test()