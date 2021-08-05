import time

from openpibo.pibo import Edu_Pibo

def msg_device(msg):
    print(msg)

def device_thread_test():
    pibo = Edu_Pibo()
    ret=pibo.start_devices(msg_device)
    print(ret)
    time.sleep(12)
    pibo.stop_devices()

if __name__ == "__main__":
    device_thread_test()