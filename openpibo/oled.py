from .modules.oled import ssd1306, board, busio, digitalio
from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps
import cv2
import os
current_path = os.path.dirname(os.path.abspath(__file__))

class Oled:
  """
  파이보의 OLED를 통해 다양한 그림을 표현합니다.

  * 사진 보기
  * 글자 나타내기
  * 도형 그리기

  example::

    pibo_oled = Oled()
  """

  def __init__(self):
    """
    Oled 클래스를 초기화
    """

    self.width = 128
    self.height = 64
    self.font_path = current_path+"/data/models/KDL.ttf" # KoPub Dotum Light
    self.font_size = 10

    spi = busio.SPI(11, 10, 9)
    rst_pin = digitalio.DigitalInOut(board.D24) # any pin!
    cs_pin = digitalio.DigitalInOut(board.D8)    # any pin!
    dc_pin = digitalio.DigitalInOut(board.D23)    # any pin!

    self.oled = ssd1306.SSD1306_SPI(self.width, self.height, spi, dc_pin, rst_pin, cs_pin)
    self.font = ImageFont.truetype(self.font_path, self.font_size)
    self.image = Image.new("1", (self.width, self.height))
    self.oled.fill(0)
    self.oled.show()

  def set_font(self, filename=None, size=None):
    """
    oled에 사용할 폰트를 설정합니다.

    example::

      pibo_oled.set_font('/home/pi/.../font.ttf', 10)
    
    :param str filename: 폰트 파일 이름

      폰트 확장자는 **ttf** 와 **otf** 모두 지원합니다.

    :param int size: 폰트 사이즈

      초기화 시 default는 10 입니다.
    """

    if filename == None:
      filename = self.font_path
    if size == None:
      size = self.font_size
    self.font = ImageFont.truetype(filename, size)

  def draw_text(self, points, text):
    """
    문자 그리기(한글, 영어 지원)

    example::

      pibo_oled.draw_text((10, 10), '안녕하세요!')

    :param tuple(int, int) points: 문자열 좌측상단 좌표 (x, y)

    :param str text: 문자열 내용
    """

    draw = ImageDraw.Draw(self.image)
    draw.text(points, text, font=self.font, fill=255)

  def draw_image(self, filename):
    """
    그림 그리기 
    
    **128x64** 크기의 **png** 확장자만 허용됩니다.

    example::
    
      pibo_oled.draw_image('/home/pi/.../image.png')

    :param str filename: 그림파일 경로
    """

    self.image = Image.open(filename).convert('1')

  def draw_data(self, img):
    """
    numpy 이미지 데이터를 입력받아 이미지로 변환합니다.

    카메라 출력값을 OLED화면에 띄우기 위해 사용됩니다.

    example::

      img = pibo_camera.read(128, 64)
      pibo.draw_data(img)
      pibo.show()

    :param numpy.ndarray img: 이미지 객체
    """
    self.image = Image.fromarray(img).convert('1')

  def draw_rectangle(self, points, fill=None):
    """
    사각형 그리기

    example::

      pibo_oled.draw_rectangle((10, 10, 80, 40), True)
    
    :param tuple points: 사각형의 좌측상단 좌표, 사각형의 우측하단 좌표 (x, y, x1, y1)
    
    :param bool fill: 채움.

      * ``True`` : 사각형 내부를 채웁니다.
      * ``False`` : 사각형 내부를 채우지 않습니다.
    """

    draw = ImageDraw.Draw(self.image)
    draw.rectangle(points, outline=1, fill=fill)

  def draw_ellipse(self, points, fill=None):
    """
    원 그리기

    example::

      pibo_oled.draw_ellipse((10, 10, 80, 40), False)

    :param tuple points: 원을 둘러 싼 사각형의 좌측상단 좌표, 사각형의 우측하단 자표 (x, y, x1, y1)

    :param bool fill: 채움.

      * ``True`` : 사각형 내부를 채웁니다.
      * ``False`` : 사각형 내부를 채우지 않습니다.
    """

    draw = ImageDraw.Draw(self.image)
    draw.ellipse(points, outline=1, fill=fill)

  def draw_line(self, points):
    """선 그리기

    example::

      pibo_oled.draw_line((30, 20, 60, 50))
    
    :param points points: 선의 시작 좌표, 선의 끝 좌표 (x, y, x1, y1)
    
    """

    draw = ImageDraw.Draw(self.image)
    draw.line(points, fill=True)

  def invert(self):
    """
    이미지를 흑백 반전시킨다.
    
    example::
    
      pibo_oled.invert()
    
    """
    self.image = self.image.convert("L")
    self.image = PIL.ImageOps.invert(self.image)
    self.image = self.image.convert("1")
  
  def show(self): 
    """
    화면에 표시하기
    
    이 메서드를 사용하지 않으면 화면에 출력되지 않습니다.
    
    example::
    
      pibo_oled.show()
    """
    
    self.oled.image(self.image)
    self.oled.show()
 
  def clear(self):
    """
    OLED 화면을 지웁니다.
    
    example::
    
      pibo_oled.clear()
    """

    self.image = Image.new("1", (self.width, self.height))
    self.oled.fill(0)
    self.oled.show()

  def size_check(self, filename):
    """
    이미지의 크기를 확인합니다.

    주로 oled의 크기인 128x64 사이즈인지 확인하기 위해 사용됩니다.

    example::

      pibo_oled.size_check('/home/pi/.../image.png')
    
    :param str filename: 확인 할 파일 경로

    :returns: 이미지의 크기

      tuple 타입 입니다.

      ``(y축 길이, x축 길이, 채널 수)`` 로 표현됩니다.
    """

    return cv2.imread(filename).shape
