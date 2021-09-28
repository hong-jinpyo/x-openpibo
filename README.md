# x-openpibo Guide

> PIBO 교육용 라이브러리입니다.

## INDEX
* [설치 및 설정](#설치-및-설정)
* [사용법](#사용법)
  + [라이브러리 사용법](#라이브러리-사용법)
  + [Tools](#Tools)
* [공식 문서](#공식-문서)


## Setting

1. 파이보 microSD 카드에 `CIRCULUS_EDU_OS`가 기본적으로 설치되어있습니다.

2. 파이보와 PC를 같은 네트워크에 접속합니다.

3. 파이보 전원을 켜서 OLED패널에 표시된 IP주소를 확인합니다.

   ![](docs/source/notes/images/ip.jpg)

4. SSH로 파이보에 접속합니다.

   ```bash
   ssh pi@<IP주소>
   # ssh pi@192.168.2.144
   ```

5. STT, TTS 기능을 사용하기 위해 [카카오 api키를 발급받습니다.](https://github.com/themakerrobot/x-openpibo/tree/master/docs/kakao_api.md)

더 자세한 설명은 [공식 문서](http://127.0.0.1:5500/x-openpibo/docs/build/html/notes/setting.html)를 참고하시기 바랍니다.

## Usage

- `openpibo` 는 아래와 같이 사용할 수 있습니다.

- 첫째로, class를 import 하고 instance를 생성합니다.

   class의 종류는 다음과 같습니다.

   ```
   audio:   Audio
   collect: Wikipedia, Weather, News
   device:  Device
   motion:  Motion, PyMotion
   oled:    Oled
   speech:  Speech, Dialog
   vision:  Camera, Face, Detect
   ```

```python
>>> from openpibo.<라이브러리 명> import <클래스 명>
  # from openpibo.audio import Audio
```

```python
>>> <인스턴스 명> = <클래스 명>()
  # pibo_audio = Audio()
```

- 다음으로 원하는 기능의 메소드를 사용합니다.

```python
>>> <인스턴스 명>.<메소드 명>(<인자>)
  # pibo_audio.play('/home/pi/openpibo-files/data/audio/test.mp3')
```

클래스 및 메소드의 종류 등 더 자세한 내용은 [공식 문서](http://127.0.0.1:5500/x-openpibo/docs/build/html/libraries/audio.html)의 LIBRARIES 탭에서 확인하실 수 있습니다.

## 공식 문서

아래 공식 문서에서 라이브러리에 대한 더욱 자세한 설명을 보실 수 있습니다.

https://themakerrobot.github.io/x-openpibo/build/html/index.html
