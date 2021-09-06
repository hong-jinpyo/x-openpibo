"""
``mp3`` , ``wav`` 파일을 재생 및 정지합니다.
"""

import os

HIGH = 1
LOW = 0

class Audio:
  """
  ``mp3`` , ``wav`` 파일을 재생 및 정지합니다.

  example::

    pibo_audio = Audio()

  """
  # out: local/hdmi/both
  # volume: mdB
  # filename: mp3/wav
  def __init__(self):
    os.system('gpio mode 7 out')
    os.system(f'gpio write 7 {HIGH}')

  def play(self, filename, out='local', volume='-2000', background=True):
    """
    ``mp3`` 또는 ``wav`` 파일을 재생합니다.

    example::

      pibo_audio.play('/home/pi/.../test.mp3', 'local', '-2000', True)
        
    :param str filename: 재생할 파일의 경로.
    
      ``mp3`` 와 ``wav`` 형식을 지원합니다.

    :param str out: 출력 대상을 설정합니다.
    
      ``local``, ``hdmi``, ``both`` 만 입력할 수 있습니다.
      
      (default: ``local``)

    :param str or int volume: 음량을 설정합니다.
    
      단위는 ``mdB`` 이고, 값이 커질수록 음량이 커집니다.
      
      음량이 매우 크므로 ``-2000`` 정도로 사용하는 것을 권장합니다.

      (default: ``-2000``)

    :param bool background: 오디오 파일을 백그라운드에서 실행할지 여부를 결정합니다.

      * ``True``: 오디오 재생 중에 다른 명령어를 사용할 수 있습니다. (default)
      * ``False``: 오디오 파일이 종료될 때 까지 다른 명령어를 실행할 수 없습니다.
    """

    if background:
      os.system("omxplayer -o {} --vol {} {} &".format(out, volume, filename))
    else:
      os.system("omxplayer -o {} --vol {} {}".format(out, volume, filename))

  def stop(self):
    """background에서 재생중인 오디오를 정지합니다.
    
    example::
    
      pibo_audio.stop()"""

    os.system('sudo pkill omxplayer')
  
  def mute(self, value):
    """파이보를 무음모드로 만듭니다.
    
    :param bool value:
    
      * ``True``: 무음모드
      * ``False``: 무음모드 해제."""

    if type(value) != bool:
      raise TypeError(f"'{value}' is not a bool.")
    if value:
      os.system(f'gpio write 7 {LOW}')
    else:
      os.system(f'gpio write 7 {HIGH}')