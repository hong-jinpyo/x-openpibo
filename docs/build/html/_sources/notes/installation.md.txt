# Installation

1. 파이보 SD카드에 `CIRCULUS_EDU_OS`를 설치

2. wifi 연결하기
   
   - SD카드 `boot` 디렉토리에서 `wpa_supplicant.conf` 파일을 수정합니다.

     ```
     country=KR
     ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
     network={
         ssid="YOUR_NETWORK_NAME"
         psk="YOUR_PASSWORD"
         key_mgmt=WPA-PSK
     }
     ```

     - `YOUR_NETWORK_NAME` : 접속하려는 wifi 주소로 수정
     - `YOUR_PASSWORD` : wifi 주소의 비밀번호로 수정

   - SD카드로 부팅을 하게되면 `wpa_supplicant.conf` 파일이 사라집니다.

      만약 새로운 네트워크에 접속하려면, `wpa_supplicant.conf.bak` 파일을 복사하여
      
      새로운 `wpa_supplicant.conf` 를 만들어 wifi 설정 후 사용하시면 됩니다.

3. 파이보에 SD카드 결합 후 전원 on

4. 컴퓨터에서도 파이보와 같은 네트워크에 접속

5. 컴퓨터에서 파이보로 ssh 접속

   **Terminal** (windows 에서는 **PowerShell**) 을 켜고 다음과 같이 입력

   ```bash
   ssh pi@<xxx.xxx.xxx.xxx>
   
   pi@xxx.xxx.xxx.xxx's password: raspberry
   ```

   > pi@ 뒤에는 파이보 OLED에 표시된 ip번호를 입력합니다.
   >
   > 초기 비밀번호는 `raspberry`로 설정되어 있습니다.

# Option

1. TTS(Text to Speech), STT(Speech to Text) 등의 기능을 사용하기 위해서는 `KAKAO REST API KEY` 가 있어야 합니다.

   해당 설정을 하는 방법은 [여기](https://themakerrobot.github.io/x-openpibo/build/html/notes/kakao_api.html)를 참고해주세요.

2. 각종 x-openpibo 패키지와 도구들을 설치하는 방법입니다.

   데이터 유실 등의 이유로 패키지와 도구를 재설치 할 때 사용합니다.

   - 패키지 설치

      ```bash
      $ sudo pip3 install git+https://github.com/themakerrobot/x-openpibo
      
      # 또는
      
      $ git clone https://github.com/themakerrobot/x-openpibo.git
      $ cd x-openpibo
      $ sudo python3 setup.py install
      ```

   - 추가 도구 설치

      ```bash
      # 각종 툴
      $ git clone https://github.com/themakerrobot/x-openpibo-tools.git

      # 예제 코드
      $ git clone https://github.com/themakerrobot/x-openpibo-example.git
      
      # 샘플 데이터
      $ git clone https://github.com/themakerrobot/x-openpibo-data.git
      ```
