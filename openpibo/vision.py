"""
`OpenCV` 라이브러리를 활용한 PIBO의 영상처리 관련 라이브러리입니다. (Local 실행 제약)

카메라 기능, 얼굴 인식, 객체/바코드/문자 인식을 수행합니다.
"""

import cv2
import dlib
import numpy as np
import pytesseract
from pyzbar import pyzbar
import pickle,os,time
from .modules.vision.stream import VideoStream
import os
current_path = os.path.dirname(os.path.abspath(__file__))

class Camera:
  """
  파이보의 카메라를 제어합니다.

  * 사진 촬영, 읽기, 쓰기, 보기 등 카메라 기본 기능을 사용할 수 있습니다.
  * Streaming, Cartoonize 기능을 사용할 수 있습니다.

  example::

    pibo_camera = Camera()
  """

  def __init__(self):
    """
    Camera 클래스를 초기화 합니다.
    """
    os.system('v4l2-ctl -c vertical_flip=1,horizontal_flip=1,white_balance_auto_preset=3')

  def imread(self, filename):
    """
    이미지 파일을 읽습니다.

    example::

      pibo_camera('/home/pi/.../image.jpg')
    
    :param str filename: 사용할 이미지 파일

    :returns: ``numpy.ndarray`` 타입 이미지 객체
    """

    return cv2.imread(filename)

  def read(self, w=640, h=480):
    """
    카메라를 통해 이미지를 촬영합니다.

    해상도 변경 시 이미지가 깨질 수 있으므로, 기본 해상도를 권장합니다.

    example::

      pibo_camera.read(640, 480)
    
    :param int w: 촬영할 이미지의 가로 픽셀 크기 입니다.

      w의 최댓값은 2592 입니다.

    :param int h: 촬영할 이미지의 세로 픽셀 크기 입니다.

      h의 최댓값은 1944 입니다.

    :returns: ``numpy.ndarray`` 타입 이미지 객체
    """

    vs = VideoStream(width=w, height=h).start()
    img = vs.read()
    vs.stop()
    return img

  def imwrite(self, filename, img):
    """
    이미지를 파일로 저장합니다.

    example::

      img = pibo.camera.read(640, 480)
      pibo_camera.imwrite('/home/pi/.../image.jpg', img)
    
    :param str filename: 저장할 파일 이름

    :param numpy.ndarray img: 저장할 이미지 객체 
    """

    return cv2.imwrite(filename, img)

  def imshow(self, img, title="IMAEGE"):
    """
    모니터에서 이미지를 확인합니다. (GUI 환경에서만 동작)

    ``cannot connect to X server`` 에러가 발생하는 이유는 GUI환경이 아니기 때문입니다.

    정상 동작을 위해서는 GUI 환경이 구축된 OS에서 시도합니다.

    example::

      img = pibo.camera.read(640, 480)
      pibo_camera.imshow(img, 'IMAGE')

    :param numpy.ndarray img: 보여줄 이미지

    :param str title: 윈도우 창 타이틀
    """

    return cv2.imshow(title, img)

  def waitKey(self, timeout=1000):
    """
    이미지를 보는 시간을 설정합니다.

    **imshow** 함수와 함께 사용합니다. (GUI 환경에서만 동작)

    ``cannot connect to X server`` 에러가 발생하는 이유는 GUI환경이 아니기 때문입니다.

    정상 동작을 위해서는 GUI 환경이 구축된 OS에서 시도합니다.

    example::

      pibo_camera.waitKey(1000)
    
    :param int timeout: 이미지를 보는 시간(ms)
    """

    return cv2.waitKey(timeout)

  def streaming(self, w=640, h=480, timeout=5):
    """
    모니터에서 이미지를 스트리밍합니다. (GUI 환경에서만 동작)

    ``cannot connect to X server`` 에러가 발생하는 이유는 GUI환경이 아니기 때문입니다.

    정상 동작을 위해서는 GUI 환경이 구축된 OS에서 시도합니다.

    :param int w: 사진의 width 값
    
    :param int h: 사진의 height 값

    :param int timeout: 스트리밍 시간
    """

    vs = VideoStream(width=w, height=h).start()
    t = time.time()

    while True:
      img = vs.read()
      cv2.imshow("show", img)
      cv2.waitKey(1)
      if time.time() - t > timeout:
        break
    vs.stop()
    return True

  def rectangle(self, img, p1, p2, color=(255,255,255), tickness=1):
    """
    이미지에 사각형을 그립니다.

    example::

      img = pibo_camera.read()
      pibo_camera.rectangle(img, (10, 10), (300, 200), (255, 255, 255), 1)
    
    :param numpy.ndarray img: 이미지 객체

    :param tuple(int, int) p1: 좌측상단 좌표 (x, y)

    :param tuple(int, int) p2: 우측하단 좌표 (x, y)

    :param tuple(int, int, int) color: RGB 값 (r, g, b)

    :param int tickness: 사각형 모서리의 두께 (픽셀 값입니다)
    """

    return cv2.rectangle(img, p1, p2, color, tickness)

  def putText(self, img, text, p, size=1, color=(255,255,255), tickness=1):
    """
    이미지에 문자를 입력합니다. (영어만 가능)

    example::

      img = pibo_camera.read()
      new_img = pibo_camera.putText(img, 'hello', (15, 10), 10, (255, 255, 255), 1)

    :param numpy.ndarray img: 이미지 객체

    :param str text: 표시할 문자열

    :param tuple(int, int) p: 좌측상단 좌표 (x, y)

    :param int size: 표시할 글자의 크기

    :param tuple(int, int, int) color: 글자 색깔 RGB 값 (r, g, b)

    :param int tickness: 글자 두께
    """
    # :returns: text가 입혀진 ``numpy.ndarray`` 이미지 객체

    # 아래 주석을 해제하면 한글 사용 가능.
    # 단, cv2가 아닌 PIL을 사용하기 때문에 return 으로 이미지를 받아 사용해야 됨.

    # from PIL import ImageFont, ImageDraw, Image

    # size = int(size*30)
    # fontpath = current_path+'/data/models/KDL.ttf'
    # font = ImageFont.truetype(fontpath, size)
    # img_pil = Image.fromarray(img)
    # draw = ImageDraw.Draw(img_pil)
    # draw.text(p, text, font=font, fill=color)
    # img = np.array(img_pil)
    # return img

    return cv2.putText(img, text, p, cv2.FONT_HERSHEY_SIMPLEX, size, color, tickness)

  def cartoonize(self, img):
    """
    만화같은 이미지로 변경합니다.

    example::

      img = pibo_camera.read()
      new_image = pibo_camera.cartoonize(img)
    
    :param numpy.ndarray img: 이미지 객체

    :returns: 변환된 ``numpy.ndarray`` 이미지 객체
    """

    numDownSamples = 2 # number of downscaling steps
    numBilateralFilters = 7  # number of bilateral filtering steps

    # -- STEP 1 --
    # downsample image using Gaussian pyramid
    img_color = img
    for _ in range(numDownSamples):
      img_color = cv2.pyrDown(img_color)

    # repeatedly apply small bilateral filter instead of applying
    # one large filter
    for _ in range(numBilateralFilters):
      img_color = cv2.bilateralFilter(img_color, 9, 9, 7)

    # upsample image to original size
    for _ in range(numDownSamples):
      img_color = cv2.pyrUp(img_color)

    # -- STEPS 2 and 3 --
    # convert to grayscale and apply median blur
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)

    # -- STEP 4 --
    # detect and enhance edges
    img_edge = cv2.adaptiveThreshold(img_blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 7)

    # -- STEP 5 --
    # convert back to color so that it can be bit-ANDed
    # with color image
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    return cv2.bitwise_and(img_color, img_edge)
 
  def convert_img(self, img, w=128, h=64):
    """
    이미지의 크기를 변환합니다.

    example::

      img = pibo_camera.read()
      pibo_camera.convert_img(img, 128, 64)

    :param numpy.ndarray img: 이미지 객체

    :param int w: 변환될 이미지의 가로 크기입니다. (픽셀 단위)

    :param int h: 변환될 이미지의 세로 크기입니다. (픽셀 단위)

    :returns: 크기 변환 후의 이미지 객체
    """

    img = cv2.resize(img, (w, h))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

  def rotate10(self, img):
    """
    이미지를 반시계 방향으로 10도만큼 회전시킵니다.

    example::

      img = pibo_camera.read()
      pibo_camera.rotate10(img)
    
    :param numpy.ndarray img: 이미지 객체

    :returns: 10도 회전한 ``numpy.ndarray`` 이미지 객체
    """

    rows, cols = img.shape[0:2]
    m10 = cv2.getRotationMatrix2D((cols/2,rows/2), 10, 0.9)
    img = cv2.warpAffine(img, m10, (cols,rows))
    return img

  def bgr_hls(self, img):
    """
    BGR 이미지 모델을 HLS 이미지 모델로 변환한다.

    BGR: Blue, Green, Red

    HLS: Hue(색상), Luminance(명도), Saturation(채도)

    example::

      img = pibo_camera.read()
      new_img = pibo_camera.bgr_hls(img)
    
    :param numpy.ndarray img: 이미지 객체

    :returns: 변환된 ``numpy.ndarray`` 이미지 객체
    """

    return cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

class Face:
  """
  얼굴과 관련된 다양한 기능을 수행하는 클래스 입니다.

  * 얼굴을 탐색합니다.
  * 얼굴을 학습/저장/삭제합니다.
  * 학습된 얼굴을 인식합니다.
  * 얼굴로 나이/성별을 추정합니다.

  인스턴스마다 **facedb** 를 가지고 있으며, 여기에서 얼굴 데이터를 등록하고 불러오고 삭제합니다.

  example::

    pibo_face = Face()
  """

  def __init__(self):
    self.model_path = current_path+"/data/models"
    self.facedb = [[],[]]
    self.threshold = 0.4
    self.age_class = ['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']
    self.gender_class = ['Male', 'Female']
    self.agenet = cv2.dnn.readNetFromCaffe(
                 self.model_path+"/deploy_age.prototxt",
                 self.model_path+"/age_net.caffemodel")
    self.gendernet = cv2.dnn.readNetFromCaffe(
                    self.model_path+"/deploy_gender.prototxt",
                    self.model_path+"/gender_net.caffemodel")
    self.face_detector = cv2.CascadeClassifier(self.model_path + "/haarcascade_frontalface_default.xml")
    self.predictor = dlib.shape_predictor(self.model_path + "/shape_predictor_5_face_landmarks.dat")
    self.face_encoder = dlib.face_recognition_model_v1(self.model_path + "/dlib_face_recognition_resnet_model_v1.dat")
  
  def get_db(self):
    """
    사용중인 얼굴 데이터베이스를 확인합니다.

    example::

      pibo_face.get_db()

    :returns: **facedb** (``list(list, list)`` 타입)
    """

    return self.facedb

  def init_db(self):
    """
    얼굴 데이터베이스를 초기화 합니다.

    초기화된 데이터베이스는 빈 이중 list ``[[], []]`` 입니다.

    첫 번째 list에는 얼굴의 이름이, 두 번째 list에는 학습된 얼굴 데이터가 인코딩되어 들어갑니다.
    
    example::

      pibo_face.init_db()
    """

    self.facedb = [[], []]

  def load_db(self, filename):
    """
    얼굴 데이터베이스 파일을 불러옵니다.

    example::

      pibo_face.load_db('/home/pi/.../facedb')

    :param str filename: 불러 올 ``facedb`` 파일의 경로입니다.
    """

    with open(filename, "rb") as f :
      self.facedb = pickle.load(f)
  
  def save_db(self, filename):
    """
    얼굴 데이터베이스를 파일로 저장합니다.

    example::

      pibo_face.save_db('/home/pi/.../facedb')
    
    :param str filename: 저장 할 ``facedb`` 파일의 경로입니다.
    """

    with open(filename, "w+b") as f:
      pickle.dump(self.facedb, f)

  def train_face(self, img, face, name):
    """
    얼굴을 학습합니다.

    학습된 얼굴은 ``get_db`` 메서드로 확인할 수 있습니다.

    example::

      pibo.camera = Camera()
      img = pibo_camera.read()

      faces = pibo_face.detect()
      face = faces[n] # face는 faces중 하나
      pibo_face.train_face(img, face, 'honggildong')
    
    :param numpy.ndarray img: 이미지 객체

    :param numpy.ndarray face: 얼굴의 좌표 (x1, y1, x2, y2)

    :param str name: 저장할 얼굴의 이름
    """

    x,y,w,h = face
    rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    shape = self.predictor(gray, rect)
    face_encoding = np.array(self.face_encoder.compute_face_descriptor(img, shape, 1))

    self.facedb[0].append(name)
    self.facedb[1].append(face_encoding)
    #cv2.imwrite(self.data_path+"/{}.jpg".format(name), img[y+3:y+h-3, x+3:x+w-3]);

  def delete_face(self, name):
    """
    등록된 얼굴을 삭제합니다.

    example::

      pibo_face.delete_face('honggildong')
    
    :param str name: 삭제할 얼굴의 이름

    :returns: ``True`` / ``False``
    """

    ret = name in self.facedb[0]
    if ret == True:
      idx = self.facedb[0].index(name)
      #os.remove(self.data_path +"/" + name + ".jpg")
      for item in self.facedb:
        del item[idx]

    return ret

  def recognize(self, img, face):
    """
    등록된 얼굴을 인식합니다.

    example::

      img = pibo_camera.read()
      face = pibo_face.detect(img)[0]
      pibo_face.recognize(img, face)
    
    :param numpy.ndarray img: 이미지 객체

    :param numpy.ndarray face: 얼굴의 좌표 (x, y, w, h)

    :returns dict: ``{"name": 이름, "score": 오차도}``

      얼굴이 비슷할수록 오차도가 낮게 측정됩니다.

      오차도가 0.4 이하일 때 동일인으로 판정합니다.
    """

    if len(self.facedb[0]) < 1:
      return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data={"name":"Guest", "score":0}
    (x,y,w,h) = face
    rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
    shape = self.predictor(gray, rect)
    face_encoding = np.array(self.face_encoder.compute_face_descriptor(img, shape, 1))
    matches = []
    matches = list(np.linalg.norm(self.facedb[1] - face_encoding, axis=1))
    data["score"] = round(min(matches), 2)

    if min(matches) < self.threshold:
      data["name"] = self.facedb[0][matches.index(min(matches))]
    return data
  
  def detect(self, img):
    """
    얼굴을 탐색합니다.

    example::

      img = pibo_camera.read()
      pibo_face.detect(img)

    :param numpy.ndarray img: 이미지 객체

    :returns: 인식된 얼굴들의 (x, y, w, h) 배열 입니다.
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = self.face_detector.detectMultiScale(gray, 1.1, 5)
    #(x,y,w,h) = faces[0]
    return faces

  def get_ageGender(self, img, face):
    """
    얼굴의 나이, 성별을 추정합니다.

    example::

      img = pibo_camera.read()
      face = pibo_face.detect(img)[0]
      pibo_face.get_ageGender(img, face)
    
    :param numpy.ndarray img: 이미지 객체

    :param numpy.ndarray face: 얼굴의 좌표 (x, y, w, h)

    :returns dict: ``{"age": 나이, "gender": 성별}``

      * age: 나이의 범위를 tuple() 형태로 출력한다.
      
        ex) (15, 20) # 15살에서 20살 정도
    
    참고: https://github.com/kairess/age_gender_estimation
    """

    data = []

    x1, y1, w, h = face
    x2 = x1+w
    y2 = y1+h

    face_img = img[y1:y2, x1:x2].copy()
    blob = cv2.dnn.blobFromImage(face_img, scalefactor=1, size=(227, 227),
      mean=(78.4263377603, 87.7689143744, 114.895847746),
      swapRB=False, crop=False)

    # predict gender
    self.gendernet.setInput(blob)
    gender_preds = self.gendernet.forward()
    gender = self.gender_class[gender_preds[0].argmax()]

    # predict age
    self.agenet.setInput(blob)
    age_preds = self.agenet.forward()
    age = self.age_class[age_preds[0].argmax()]

    data = {"age":age, "gender":gender}

    # visualize
    #cv2.rectangle(img, (x1, y1), (x2, y2), (255,255,255), 2)
    #cv2.putText(img, "{} {}".format(gender, age), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,128,128), 2)
    return data

class Detect:
  """
  얼굴 인식과 관련된 다양한 기능을 사용할 수 있는 클래스 입니다.

  * 20개 class 안에서의 객체 인식 (MobileNetSSD)
  * QR/바코드 인식 (pyzbar)
  * 문자 인식(OCR, Tesseract)

  example::

    pibo_detect = Detect()
  """

  def __init__(self):
    self.model_path = current_path+"/data/models"
    self.object20_class = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
                    "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike",
                    "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    self.mobilenet = cv2.dnn.readNetFromCaffe(
                   self.model_path+"/MobileNetSSD_deploy.prototxt.txt",
                   self.model_path+"/MobileNetSSD_deploy.caffemodel")

  def detect_object(self, img):
    """
    이미지 안의 객체를 인식합니다. (20개 class의 사물 인식 가능)

    인식 가능한 사물은 다음과 같습니다::

      "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", 
      "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", 
      "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"

    example::

      img = pibo_camera()
      pibo_detect.detect_object(img)
    
    :param numpy.ndarray img: 이미지 객체

    :returns: ``{"name":이름, "score":정확도, "position":사물좌표(startX, startY, endX, endY)}``

      * score는 0~100 사이의 float 값 입니다.
    """

    data = []
    (h, w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)
    self.mobilenet.setInput(blob)
    detections = self.mobilenet.forward()

    for i in np.arange(0, detections.shape[2]):
      confidence = detections[0, 0, i, 2]
      if confidence > 0.2:
        idx = int(detections[0, 0, i, 1])
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        data.append({"name":self.object20_class[idx], "score":confidence * 100, "position":(startX,startY,endX,endY)})
        # draw the prediction on the frame
        #label = "{}: {:.2f}%".format(self.object20_class[idx], confidence * 100)
        #cv2.rectangle(img, (startX, startY), (endX, endY), (128,0,128), 2)
        #y = startY - 15 if startY - 15 > 15 else startY + 15
        #cv2.putText(img, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,128,128), 2)
    return data

  def detect_qr(self, img):
    """
    이미지 안의 QR코드 및 바코드를 인식합니다.

    example::

      img = pibo_camera()
      pibo_detect.detect_qr(img)
    
    :param numpy.ndarray img: 이미지 객체

    :returns: ``{"type": 바코드 / QR코드 , "data":내용}``
    """

    barcodes = pyzbar.decode(img)
    return {"data":barcodes[0].data.decode("utf-8"), "type":barcodes[0].type} if len(barcodes) > 0  else {"data":"", "type":""}

  def detect_text(self, img):
    """
    이미지 안의 문자를 인식합니다.

    example::

      img = pibo_camera()
      pibo_detect.detect_text(img)

    :param numpy.ndarray: 이미지 객체

    :returns: 인식된 문자열
    """

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return pytesseract.image_to_string(img_rgb, lang='eng+kor', config=r'--oem 3 --psm 6')
