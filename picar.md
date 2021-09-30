# Picar PJT guide

> tracking module과 openCV를 이용한 line tracing 구현
>
> 본 프로젝트는 x-openpibo의 picar branch에서 확인할 수 있습니다.



## 샘플코드 실행

> x-openpibo/ 경로에 있음

- tracking module을 이용한 로직 실행

  ```
  sudo python3 ~/x-openpibo/picar_tracking.py
  ```
  
- openCV를 이용한 로직 실행

  ```
  sudo python3 ~/x-openpibo/picar_CVtracking.py
  ```



## 라이브러리

> x-openpibo/openpibo/picar_lib 경로에 있음
>
> class 단위로 picar 각 부품을 컨트롤할 수 있도록 구현 (파이보와 유사하게)



### class

- DCMotor

  - 동력원인 뒷바퀴의 모터를 컨트롤하는 class

  - move 메소드에서 좌회전 또는 우회전을 할 때 turn 인자를 전달받아 양쪽 바퀴의 RPM의 차이를 둠.

- ServoMotor

  - PCA9685에 pwm 신호로 통신

  - 16개 모터 핀 중 3개만 사용하며, 각 핀에 등록된 모터는 다음과 같음

    0: 앞바퀴 조향, 1: 카메라 좌우, 2: 카메라 상하

- Tracking

  - picar 앞바퀴 사이 하단부에 부착된 tracking module로 검은 선을 찾음
  - 왼쪽, 중간, 오른쪽에 센서가 달려있어 검은 선이 가운데 센서에만 인식될 수 있도록 하며 tracking이 가능.

- Camera

  - openCV를 사용해 라인 디텍팅

  - 라인 디텍팅 로직은 다음과 같음

    이미지 캡쳐

    -> 흑백 변환

    -> OTSU 알고리즘으로 이진화 (OTSU: 이진화시 임계값을 계산하는 알고리즘)

    -> 이미지 하단부 두 줄 (y축 380, 440 라인)에 디텍팅 된 검은 선들 중 지정된 두께와 유사한 선을 찾아 `라인`ㅇ로 인식

    -> 라인의 위치 반환



## OpenCV linefinder web으로 보기

> openCV으로 찾은 라인을 시각화하여 볼 수 있는 모듈



- 실행방법

  ```
  sudo python3 ~/x-openpibo/CVtracking_web/app.py
  ```

  이후 브라우저로 웹에 접속

