"""
PIBO의 움직임을 제어합니다.

:모터 번호당 위치:

  * 0번 : 'Right Foot'
  * 1번 : 'Right Leg'
  * 2번 : 'Right Arm'
  * 3번 : 'Right Hand'
  * 4번 : 'Head Pan'
  * 5번 : 'Head Tilt'
  * 6번 : 'Left Foot'
  * 7번 : 'Left Leg'
  * 8번 : 'Left Arm'
  * 9번 : 'Left Hand'

  **(파이보의 입장에서 Right, Left 입니다.)**

:모터 제한각도: 각 모터가 회전할 수 있는 범위가 제한되어있습니다.

  * 0번 : ± 25˚
  * 1번 : ± 35˚
  * 2번 : ± 80˚
  * 3번 : ± 30˚
  * 4번 : ± 50˚
  * 5번 : ± 25˚
  * 6번 : ± 25˚
  * 7번 : ± 35˚
  * 8번 : ± 80˚
  * 9번 : ± 30˚

:모션 프로파일: 모션 데이터가 저장되어있는 JSON형태의 데이터입니다.

  기본 모션 프로파일 내 모션 리스트::

    stop, stop_body, sleep, lookup, left, left_half, right, right_half, foward1-2,
    backward1-2, step1-2, hifive, cheer1-3, wave1-6, think1-4, wake_up1-3, hey1-2,
    yes_h, no_h, breath1-3, breath_long, head_h, spin_h, clapping1-2, hankshaking,
    bow, greeting, hand1-4, foot1-2, speak1-2, speak_n1-2, speak_q, speak_r1-2, 
    speak_l1-2, welcome, happy1-3, excite1-2, boring1-2, sad1-3, handup_r, 
    handup_l, look_r, look_l, dance1-5, motion_test, test1-4
    # foward1-2는 forward1, forward2 두 종류가 있음을 의미합니다.
"""

import serial
import time
import os
import json
current_path = os.path.dirname(os.path.abspath(__file__))

class Motion:
  """
  파이보의 움직임을 제어합니다.

  example::

    pibo_motion = Motion()
  """

  def __init__(self):
    """Motion 클래스 초기화"""

    self.profile_path=current_path+"/data/models/motion_db.json"
    with open(self.profile_path, 'r') as f:
      self.profile = json.load(f)

  def set_profile(self, path):
    """모션 프로파일을 설정합니다.

    모션은 **openpibo-tools** 의 `motion_creator <https://themakerrobot.github.io/x-openpibo/build/html/tools/motion_creator.html>`_ 를 이용해 생성할 수 있습니다.

    example::

      pibo_motion.set_profile('/data/models/motion_db.json')
    
    :param str path: 모터 프로파일 경로"""

    with open(path, 'r') as f:
      self.profile = json.load(f)

  def set_motor(self, no, position):
    """
    모터 1개를 측정 위치로 이동합니다.
    
    example::
    
      pibo_motion.set_motor(2, 30)
    
    :param int no: 모터 번호
    
      0~9의 숫자가 들어갑니다.
      해당 번호의 위치는 상단의 ``모터 번호당 위치`` 를 참고해주세요.
    
    :param int position: 모터 각도
    
      -80~80의 숫자가 들어갑니다.
      자세한 범위는 상단의 ``모터 제한각도`` 를 참고해주세요.
    """

    os.system("servo write {} {}".format(no, position*10))

  def set_motors(self, positions, movetime=None):
    """
    전체 모터를 특정 위치로 이동합니다.

    모션을 취하는 속도는 ``(회전각도 / movetime)`` 이므로, movetime이 짧을수록 빨라집니다.

    만약 ``movetime`` 이 ``None`` 이라면, 속도는 이전 설정값이 됩니다.
    
    example::

      pibo_motion.set_motors([0, 0, -80, 0, 0, 0, 0, 0, 80, 0])
    
    :param list position: 0-9번 모터 각도 배열
    
    :param int movetime: 모터 이동 시간(ms)
    
      50ms 단위, 모터가 정해진 위치까지 이동하는 시간
      
      (모터 컨트롤러와의 overhead문제로 정밀하지는 않음)"""

    mpos = [positions[i]*10 for i in range(len(positions))]
    
    if movetime == None:
      os.system("servo mwrite {}".format(" ".join(map(str, mpos))))
    else:
      os.system("servo move {} {}".format(" ".join(map(str, mpos)), movetime))
    return True

  def set_speed(self, n, spd):
    """
    모터 1개의 속도를 설정합니다.

    example::

      pibo_motion.set_speed(3, 255)
    
    :param int n: 모터 번호

    :param int spd: 모터 속도

      0~255 사이 값입니다.
      숫자가 클수록 속도가 빨라집니다.
    """

    os.system("servo speed {} {}".format(n, spd))

  def set_acceleration(self, n, accl):
    """
    모터 1개의 가속도를 설정합니다.

    가속도를 설정하게 되면, 속도가 0에서 시작하여 점점 빨라지고, 가속도...
    
    example::
    
      pibo_motion.set_acceleration(3, 255)
    
    :param int n: 모터 번호

    :param int accl: 모터 속도

      0~255 사이 값입니다.
      숫자가 클수록 가속도가 커집니다.
    """

    os.system("servo accelerate {} {}".format(n, accl))

  def set_speeds(self, spds):
    """
    전체 모터의 속도를 설정합니다.

    example::

      pibo_motion.set_speeds([20, 50, 40, 20, 20, 10, 20, 50, 40, 20])
    
    :param list spds: 0-9번 모터 속도 배열

      배열 안의 각 가속도는 0~255 사이 정수입니다.
    """

    os.system("servo speed all {}".format(" ".join(map(str, spds))))

  def set_accelerations(self, accls):
    """
    전체 모터의 가속도를 설정합니다.

    example::

      pibo_motion.set_accelerations([10, 10, 10, 10, 20, 20, 10, 10, 10, 10])
    
    :param list accls: 0-9번 모터 가속도 배열

      배열 안의 각 가속도는 0~255 사이 정수입니다.
    """

    os.system("servo accelerate all {}".format(" ".join(map(str, accls))))

  def get_motion(self, name=None):
    """
    모션 프로파일을 조회합니다.

    ``name`` 매개변수가 ``None`` 이면, 현재 ``profile`` 에 저장되어있는 모든 **moiton** 을 출력합니다.
    
    example::
    
      pibo_motion.get_motion('forward1')
    
    :param str name: 동작 이름

      profile에 저장되어있는 동작의 이름입니다.

      초기화 시 forward1(전진1), forward2(전진2), sleep(잠자기), dance1(춤추기1) 등을 조회할 수 있습니다.
    """

    ret = self.profile.get(name)
    ret = list(self.profile.keys()) if ret == None else ret
    return ret

  def set_motion(self, name, cycle=1):
    """
    모션 프로파일의 동작을 실행하는 ``set_motion_raw`` 메서드를 호출합니다.
    ``motion_db`` 에서 ``name`` 에 해당하는 **JSON** 형식의 데이터를 불러와 ``set_motion_raw`` 메서드에게 넘겨줍니다.

    example::

      pibo_motion.set_motion('dance1')
    
    :param str name: 동작 이름

      profile에 저장되어있는 동작의 이름입니다.

      초기화 시 forward1(전진1), forward2(전진2), sleep(잠자기), dance1(춤추기1) 등을 실행할 수 있습니다.
    
    :param int cycle:

      동작을 몇 번 반복할지 결정합니다.
    """

    exe = self.profile.get(name)
    return self.set_motion_raw(exe, cycle)
  
  def set_motion_raw(self, exe, cycle=1):
    """
    모션 프로파일의 동작을 실행합니다.

    example::

      pibo_motion.set_motion(
        '{"pos":[{"d":[ 999, 999, 999, 999,  30, 999, 999, 999, 999, 999 ],"seq": 500}]}',
        2
      )
    
    :param str exe: 특정 동작을 위한 각 모터의 움직임이 기록된 데이터 입니다.

      다음과 같은 양식을 따릅니다::

        {
          "init":[0,0,-70,-25,0,0,0,0,70,25],
          "pos":[
            {"d":[999,999,999,999, 30,999,999,999,999,999],"seq":500},
            {"d":[999,999,999,999,-30,999,999,999,999,999],"seq":2000},
            ...
          ]
        }
      
      * ``init`` 은 동작을 시작하기 전의 준비동작입니다.
      * ``pos`` 는 연속된 동작이 담긴 list 입니다.
        **seq** 시간에 **d** 의 동작이 완료됨을 의미합니다.

    :param int cycle:

      동작을 몇 번 반복할지 결정합니다.
    """

    ret = True
    if exe == None:
      ret = False
      return ret
    seq,cnt,cycle_cnt = 0,0,0
    self.stopped = False

    if exe["init_def"] == 1:
      self.set_motors(exe["init"], seq)
    
    if "pos" not in exe:
      return ret

    time.sleep(0.5)
    while True:
      if self.stopped:
        break

      d, intv = exe["pos"][cnt]["d"], exe["pos"][cnt]["seq"]-seq
      seq = exe["pos"][cnt]["seq"]

      self.set_motors(d, intv)
      time.sleep(intv/1000)
      cnt += 1
      if cnt == len(exe["pos"]):
        cycle_cnt += 1
        if cycle > cycle_cnt:
          cnt,seq = 0,0
          continue
        break
    return ret

  def stop(self):
    """
    수행중인 동작을 정지합니다.

    example::
      
      # 동작을 수행중일 때,
      pibo_motion.stop()
    """

    self.stopped = True

class PyMotion:
  """
  파이보의 움직임을 제어하는 클래스.

  ``Motion`` 클래스와의 차이점은, 모터 컨트롤러와 직접 통신한다는 점입니다.

  example::

    pibo_pymotion = PyMotion()
  """

  _defaults = {
    "device_path":"/dev/ttyACM0",
  }

  def __init__(self):
    """
    PyMotion 클래스를 초기화합니다.
    """

    self.__dict__.update(self._defaults) # set up default values
    self.dev = serial.Serial(port=self.device_path, baudrate=115200)
    self.motor_range = [25,35,80,30,50,25,25,35,80,30]

  def set_motor(self, n, degree):
    """
    모터 1개를 특정 위치로 이동합니다.

    example::

      pibo_pymotion.set_motor(3, 30)
    
    :param int n: 모터 번호. 0~9 사이의 정수입니다.

    :param int degree: 모터 각도. -80~80 사이의 정수입니다.
    
      자세한 범위는 상단의 ``모터 제한각도`` 를 참고해주세요.

    :returns: ``True`` / ``False``
    """

    ret = True

    if abs(degree) > self.motor_range[n]:
      return False, "range error ch:{} range:-{} ~ {}".format(n, -1*self.motor_range[n], self.motor_range[n])

    pos = (degree*10 + 1500)*4
    lsb = pos & 0x7f #7 bits for least significant byte
    msb = (pos >> 7) & 0x7f #shift 7 and take next 7 bits for msb
    cmd = chr(0x84) + chr(n) + chr(lsb) + chr(msb)
    self.dev.write(bytes(cmd,'latin-1'))
    return ret, ""

  def set_motors(self, d_lst): # pos array
    """
    전체 모터를 특정 위치로 이동합니다.
    
    example::
    
      pibo_pymotion.set_motors([20, 0, 0, 12, 10, 10, -10, -10, 0, 0])
    
    :param list d_lst: 0~9번 모터각도.
    
      **d_lst** 에 들어가는 범위는 상단의 ``모터 제한각도`` 와 같습니다.

    :returns: ``True`` / ``False``
    """

    ret = True

    for i in range(len(d_lst)):
      if abs(d_lst[i]) > self.motor_range[i]:
        return False, "range error ch:{} range:-{} ~ {}".format(i, -1*self.motor_range[i], self.motor_range[i])

    p_lst = [(d_lst[i]*10+1500)*4 for i in range(len(d_lst))]
    cmd = chr(0x9F) + chr(10) + chr(0)
    for pos in p_lst:
      lsb = pos & 0x7f #7 bits for least significant byte
      msb = (pos >> 7) & 0x7f #shift 7 and take next 7 bits for msb
      cmd += chr(lsb) + chr(msb)
    self.dev.write(bytes(cmd,'latin-1'))
    return ret, ""

  def set_speed(self, n, val):
    """
    모터 1개의 속도를 설정합니다.

    example::

      pibo_pymotion.set_speed(3, 255)
    
    :param int n: 모터 번호. 0~9 정수입니다.

    :param int val: 모터 속도. 0~255 정수입니다.

    :returns: ``True`` / ``False``
    """

    ret = True

    if abs(val) > 255:
      return False, "range error range: 0~255"

    lsb = val & 0x7f #7 bits for least significant byte
    msb = (val >> 7) & 0x7f #shift 7 and take next 7 bits for msb
    cmd = chr(0x87) + chr(n) + chr(lsb) + chr(msb)
    self.dev.write(bytes(cmd,'latin-1'))
    return ret, ""

  def set_acceleration(self, n, val):
    """
    모터 1개의 가속도를 설정합니다.

    example::

      pibo_pymotion.set_acceleration(3, 255)
    
    :param int n: 모터 번호. 0~9 정수입니다.

    :param int val: 모터 가속도. 0~255 정수입니다.
    
    :returns: ``True`` / ``False``
    """

    ret = True

    if abs(val) > 255:
      return False, "range error range: 0~255"

    lsb = val & 0x7f #7 bits for least significant byte
    msb = (val >> 7) & 0x7f #shift 7 and take next 7 bits for msb
    cmd = chr(0x89) + chr(n) + chr(lsb) + chr(msb)
    self.dev.write(bytes(cmd,'latin-1'))
    return ret, ""

  def set_init(self):
    """
    전체 모터를 초기 상태로 이동시킵니다.

    example::

      pibo_pymotion.set_init()

    :returns: ``True`` / ``False``
    """

    ret = True
    cmd = chr(0xA2)
    self.dev.write(bytes(cmd,'latin-1'))
    return ret, ""
