# Usage

> 아래는 `Audio` 라이브러리로 음악을 재생하는 예제입니다. 다른 라이브러리와 메서드는 좌측 **LIBRARIES** 탭을 참고해주시기 바랍니다.
>
> 가이드는 두 가지 전제 하에 작성되었습니다.
> 1. `x-openpibo-data`를 `/home/pi/` 경로에 clone 하였음.
> 2. `x-openpibo`를 `sudo pip3 install`명령어로 설치 하였음.

- 먼저 다음 명령어를 작성해 python 인터프리터 모드로 들어갑니다.

```bash
$ sudo python3
```

- 사용하고자 하는 라이브러리를 import하고, `Audio` 인스턴스를 만듭니다.

```python
>>> from openpibo.audio import Audio
>>> pibo = Audio()
```

- `play` 메서드를 사용해 음악을 재생시킵니다.
- `<오디오 데이터 경로>` 에는 절대경로, 또는 상대경로가 들어갑니다.

```python
>>> pibo.play('/home/pi/x-openpibo-data/data/audio/test.mp3')
```

- `stop` 메서드로 음악을 정지시킵니다.

```python
>>> pibo.stop()
```

- 만약 너무 긴 경로를 반복해서 입력하기 번거롭다면, `config.json` 에 경로를 저장할 수 있습니다.

```json
{"DATA_PATH": "...", "KAKAO_ACCOUNT": "..."}
```

- `config.json` 파일을 수정하기 위해서는 sudo 권한이 필요합니다.

```bash
>>> quit()

$ cd ~
$ sudo vi config.json
```

- 기본적으로 `DATA_PATH`가 `/home/pi/x-openpibo-data/data/` 경로로 설정되어있지만, 사용자 임의로 만들 수도 있습니다.

```json
{
    "DATA_PATH": "/home/pi/x-openpibo-data/data/",
    "MY_DATA_PATH": "/home/pi/x-openpibo-data/data/audio/",
    "KAKAO_ACCOUNT": "..."
}
```

- `config.json` 는 `openpibo.config` 에 저장되어 있습니다.

```python
$ sudo python3

>>> import openpibo
>>> openpibo.config
```

```
{"DATA_PATH":"/home/pi/x-openpibo-data/data/", "MY_DATA_PATH":"/home/pi/ ...}
```

- 이를 활용하여 아래와 같이 데이터를 불러올 수 있습니다.

```python
>>> from openpibo.audio import Audio
>>> import openpibo
>>> pibo = Audio()
>>> pibo.play(openpibo.config['MY_DATA_PATH'] + 'test.mp3')
>>> pibo.stop()
```