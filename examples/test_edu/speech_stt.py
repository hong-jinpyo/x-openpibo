from openpibo.pibo import Edu_Pibo

def stt_test():
    pibo = Edu_Pibo()

    ret = pibo.stt()
    print(ret)

if __name__ == "__main__":
    stt_test()