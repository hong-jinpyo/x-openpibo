# PIBO Device

![PIBO_Device](images/PIBO_Device.png)

## Audio

> mp3, wav 파일을 재생 및 정지합니다.

- omxplayer
  - 라즈베리파이에서 공식적으로 지원하는 미디어 프로그램 (오디오 및 비디오 파일 형식 재생)
  - 기본적인 명령행: `omxplayer <미디어 파일명>`

## Device

> mcu(Atmega328p)를 제어합니다.

- Atmega328p

  - 자체 운영체제가 없어 외부 프로그램에서 C언어 형태로 프로그래밍하고 코드를 보드에 업로드하는 방식으로 동작
  - 주로 외부기기(센서, LCD, 모터) 제어에 많이 사용되며, 파이보에서는 PIR sensor, Neopixel, Touch sensor 제어에 사용

  ![](images/atmega328p.JPG)

- PIR Sensor

  - 적외선 감지 센서
  - 일정한 적외선을 띈 움직임이 있는 물체 감지
  - 무한 반복 트리거 동작 방식
    - HIGH 신호가 출력되는 Delay Time 내에 인체 또는 적외선 변화가 감지되면, 출력 신호 Delay Time이 초기화되며 출력 신호 유지 상태에서 다시 카운트 시작. 인체 또는 적외선 변화가 감지되지 않은 시점에서 2초 후 출력 신호는 LOW가 됨

  ![](images/PIR_Sensor.png)

- Neopixel

     - WS281x 칩이 내장된 LED
     - 어떤 모양이든 연결 가능하며 연결 배선이 간단
     - 단일 핀으로 모든 LED 개별 제어

  ![](images/ws2812.png)

- Touch Sensor

     - PCB 하단의 터치패드를 터치하면 터치 인식
     - 기구물에 부착하여 사용 (두께 3T 이하)
     - 전원인가 시 초기 출력 HIGH, 터치 시 OUTPUT LOW
     
  ![](images/Touch-Sensor.png)

## Motion/Servo

> PIBO의 움직임을 제어합니다.

## OLED

> OLED Display에 문자나 이미지를 출력합니다.

- SSD1306
  - 데이터를 화면에 출력
  - 통신 방식에 따라 SPI Type, I2C Type 존재

  ![](images/ssd1306.jpeg)

## Speech

> Kakao 음성 API를 사용하여 PIBO에 장착되어 있는 마이크와 스피커를 통해 사람의 음성 언어를 인식하거나 합성할 수 있습니다.

- MeCab
  - 일본에서 만든 형태소 분석 엔진
  - 언어, 사전 코퍼스에 의존하지 않는 범용적인 설계
  - 품사 독립적 설계
  - 각종 스크립트 언어 바인딩 (perl / ruby / python / java / C#)

## Vision

> PIBO의 영상처리 관련 라이브러리입니다. (Local 실행 제약)
>
> 카메라 기능, 얼굴 인식, 객체/바코드/문자 인식 수행

- OpenCV (Open source Computer Vision)  --->   `import cv2`

  - 영상 처리 및 컴퓨터 비전 관련 오픈소스

  - 이미지, 영상처리, Object Detection, Motion Detection 등의 기능 제공

- Caffe

  - 딥러닝 프레임워크
  - 컴퓨터 비전 머신러닝에 특화되어 있으며 주로 C/C++ 기반으로 사용
  - Caffe Model Zoo에서 미리 훈련된 여러 네트워크를 바로 사용할 수 있음

- Dlib

  - 이미지 처리 및 기계 학습, 얼굴 인식 등을 할 수 있는 C++로 개발된 고성능의 라이브러리
  - facial landmarks를 통해 얼굴을 검출하는 기능이 많이 사용됨 (파이보에서는 5개의 face_landmarks를 찾습니다.)

- Tesseract

  - 다양한 운영체제를 지원하기 위한 OCR(Optical Character Recognition) 엔진

  - OCR 이미지로부터 텍스트를 인식하고, 추출
  - 오프라인 문자인식 기법으로 입력된 input 이미지의 특징점을 추출하고 그 특징점을 사용하여 문자 인식

- pyzbar

  - 비디오 스트림, 이미지 파일 및 이미지와 같은 다양한 소스에서 바코드를 판독할 수 있는 오픈소스 라이브러리

- numpy

  - 벡터, 행렬 등 수치 연산을 수행하는 선형대수 라이브러리
  - array(행렬) 단위로 데이터를 관리하며 이에 대해 연산 수행