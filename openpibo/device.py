"""
메인 컨트롤러를 제어합니다.

메인 컨트롤러로 `#{메시지 코드}:{메시지}!` 의 형식의 신호가 전달됩니다.

그러면 메인컨트롤러는 메시지 코드와 메시지를 파악하여 주어진 역할을 수행합니다.

:메시지 상세 설명:

  * VERSION (10)

    * get: 버전정보

  * HALT (11)

    * set: 전원종료 요청
  
  * DC_CONN (14)

    * get: DC잭 연결정보

  * BATTERY (15)

    * get: 배터리정보

  * REBOOT (17)

    * set: device 설정 초기화 요청

  * NEOPIXEL (20)
  
    * data: 255,255,255 (R,G,B)
    * set: 네오픽셀설정 (R,G,B) 양쪽 동일하게 설정

  * NEOPIXEL_FADE (21)

    * data: 255,255,255,10 (R,G,B,time)
    * set: 네오픽셀설정 (R,G,B) 양쪽 동일하게 설정 (색상 천천히 변경)

  * NEOPIXEL_BRIGHTNESS (22)

    * data: 64 (brightness)
    * set: 네오픽셀설정 밝기를 설정한다. (기본: 64)

  * NEOPIXEL_EACH (23)
  
    * data: 255,255,255,255,255,255 (left(R,G,B), right(R,G,B))
    * set: 네오픽셀설정 (R,G,B,R,G,B) 양쪽 각각 설정
    
  * NEOPIXEL_FADE_EACH (24)

    * data: 255,255,255,255,255,255,10 (left(R,G,B), right(R,G,B), time)
    * set: 네오픽셀설정 (R,G,B,R,G,B) 양쪽 각각 설정 (색상 천천히 변경)
  
  * NEOPIXEL_LOOP (25)

    * data: 10 (time)
    * set: 네오픽셀 무지개색으로 일정시간 반복
  
  * NEOPIXEL_OFFSET_SET (26)

    * data: 255,255,255,255,255,255 (left(R,G,B), right(R,G,B))
    * set: 네오픽셀 최댓값 설정 (255,255,0,255,255,0 이면, white로 설정해도 노란색으로 표현됨.)

  * NEOPIXEL_OFFSET_GET (27)

    * get: 네오픽셀 오프셋 정보
  
  * NEOPIXEL_EACH_ORG (28)

    * data: 255,255,255,255,255,255 (left(R,G,B), right(R,G,B))
    * set: 네오픽셀설정 (R,G,B,R,G,B) 양쪽 각각 설정 (OFFSET의 영향을 받지 않음)

  * PIR (30)
  
    * data: ``"on"`` or ``"off"`` (sensor on/off switch)
    * set: pir sensor ``"on"`` (활성화) / ``"off"`` (비활성화)

  * SYSTEM (40)
  
      1. PIR 감지:      ``"person"`` or ``"nobody"``
      #. Touch 감지:    ``"touch" ``or ``""``
      #. DC잭 연결감지:  ``"on"`` of ``"off"``
      #. 버튼 감지:      ``"on"`` or ``""``
      #. 시스템리셋:     not support
      #. 전원종료:       ``"on"`` or ``""``
"""

import serial
import time
from threading import Lock


class Device:
  """
  파이보의 여러가지 상태를 체크하거나, 눈 색깔을 제어합니다.

  example::

    pibo_device = Device()
  """
  def __init__(self):
    """Device 클래스를 초기화합니다."""

    self.code = {
    "VERSION":"10",
    "HALT":"11",
    "BUTTON":"13",
    "DC_CONN":"14",
    "BATTERY":"15",
    "NEOPIXEL":"20",
    "NEOPIXEL_EACH":"23",
    "PIR":"30",
    "TOUCH":"31",
    "SYSTEM":"40",
    }
    self.dev = serial.Serial(port="/dev/ttyS0", baudrate=9600)
    self.lock = Lock()

  def locked(self):
    """
    Device가 사용 중인지 확인합니다.

    :returns: ``True`` / ``False``
    """

    return self.lock.locked()

  def send_cmd(self, code, data:str=""):
    """
    Device에 메시지 코드/데이터를 전송하고 응답을 받습니다.

    example::

      pibo_device.send_cmd(20, '255,255,255')

    :param str or int code: 메시지 코드
    
      * 10 : VERSION
      * 11 : HALT
      * 14 : DC_CONN
      * 15 : BATTERY
      * 17 : REBOOT
      * 20 : NEOPIXEL
      * 21 : NEOPIXEL_FADE
      * 22 : NEOPIXEL_BRIGHTNESS
      * 23 : NEOPIXEL_EACH
      * 24 : NEOPIXEL_FADE_EACH
      * 25 : NEOPIXEL_LOOP
      * 26 : NEOPIXEL_OFFSET_SET
      * 27 : NEOPIXEL_OFFSET_GET
      * 28 : NEOPIXEL_EACH_ORG
      * 30 : PIR
      * 40 : SYSTEM
    
    :param str data: 메시지

      ``code`` 의 값에 따라 데이터의 형식이 다릅니다.

      * ``.send_cmd(20, '255,255,255')``
      * ``.send_cmd(21, '255,255,255,10')``
      * ``.send_cmd(22, '64')``
      * ``.send_cmd(23, '255,255,255,255,255,255')``
      * ``.send_cmd(24, '255,255,255,255,255,255,10')``
      * ``.send_cmd(25, '2')``
      * ``.send_cmd(26, '255,255,255,255,255,255')``
      * ``.send_cmd(28, '255,255,255,255,255,255')``
      * ``.send_cmd(30, 'on')``

      **자세한 설명은 상단 "메시지 상세 설명" 참고하시기 바랍니다**
    
    :returns str: Device로부터 받은 응답
    
    """
    return self.send_raw("#{}:{}!".format(code, data))

  def send_raw(self, raw):
    """
    Device에 실제 메시지를 전송하고 응답을 받습니다.

    example::

      pibo_device.send_raw('#20:255,255,255!')
      pibo_device.send_raw('#22:64!')
    
    :param str raw: 실제 전달되는 메시지

      ``send_cmd`` 의 **code** 와 **data** 를 다음과 같은 형식으로 조합::

        "#{code}:{data}!"

      **자세한 설명은 상단 "메시지 상세 설명" 참고하시기 바랍니다**
    
    :returns: Device로부터 받은 응답
    """
    if self.lock.locked() == True:
      return False

    self.lock.acquire()
    self.dev.write(raw.encode('utf-8'))
    data = ""
    time.sleep(0.05)
    while True:
      ch = self.dev.read().decode()
      if ch == '#' or ch == '\r' or ch == '\n':
        continue
      if ch == '!':
        break
      data += ch
    self.lock.release()
    return data