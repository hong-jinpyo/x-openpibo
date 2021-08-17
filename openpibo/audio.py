"""
Audio
~~~~~
"""


import os


HIGH = 1
LOW = 0

class Audio:
  """
  파이보의 오디오를 컨트롤 하는 클래스.

  파라미터를 받지 않습니다.

  example:
  .. code-block::
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
    입력한 경로의 파일을 재생합니다.

    :param str filename: 재생할 파일의 경로.
        `mp3`와 `wav` 형식을 지원한다.

        example:
        .. code-block::
            '/home/pi/data/audio/opening.mp3'

    :param str out: 어느 포트에서 재생할지 선택합니다.
        'local', 'hdmi', 'both'만 입력할 수 있습니다.
        default는 'local'.

    :param str volumn: 볼륨을 설정한다.
        default는 '-2000'이며, 값이 커질수록 볼륨이 커집니다.
        해당 값을 양수로 키우면 볼륨이 매우 커지므로 음수로 사용하는 것을 권장합니다.

    :param bool background: 오디오 파일을 백그라운드에서 실행할지 여부를 결정합니다.
        값이 'False'이면, 오디오 파일이 종료될 때 까지 다른 명령어를 실행할 수 없고,
        값이 'True'이면, 오디오 재생 중에 다른 명령어를 사용할 수 있습니다.
        default는 'True'.
    """
    if background:
      os.system("omxplayer -o {} --vol {} {} &".format(out, volume, filename))
    else:
      os.system("omxplayer -o {} --vol {} {}".format(out, volume, filename))

  def stop(self):
    """background에서 재생중인 오디오를 정지합니다.
    파라미터를 받지 않습니다."""
    os.system('sudo pkill omxplayer')
  
  def mute(self, value):
    """파이보를 무음모드로 만듭니다.
    
    :param bool value:
        'True'이면 무음모드, 'False'이면 무음모드 해제."""
    if type(value) != bool:
      raise TypeError(f"'{value}' is not a bool.")
    if value:
      os.system(f'gpio write 7 {LOW}')
    else:
      os.system(f'gpio write 7 {HIGH}')