# Installation

1. 파이보 SD카드에 `CIRCULUS_EDU_OS`를 설치

2. SD카드 `boot` 레포지토리에서 파일을 생성 및 수정

   - `ssh` 라는 이름의 빈 파일 생성

   - `wpa_supplicant.conf`  파일 수정

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

3. 파이보에 SD카드 결합 후 전원 on

4. 컴퓨터에서도 파이보와 같은 네트워크에 접속

5. 컴퓨터에서 파이보로 ssh 접속

   Terminal을 켜고 다름과 같이 입력

   ```bash
   ssh pi@<xxx.xxx.xxx.xxx>
   
   pi@xxx.xxx.xxx.xxx's password: raspberry
   ```

   > pi@ 뒤에는 파이보 OLED에 표시된 ip번호를 입력합니다.
   >
   > 초기 비밀번호는 `raspberry`로 설정되어 있습니다.

6. `lxml` 파서를 설치합니다. `추후 수정 요. os에서 미리 설치`

   ```bash
   sudo apt-get install python3-lxml -y
   ```

7. 각종 x-openpibo 패키지와 도구들을 설치합니다.

   - 패키지 설치

      ```bash
      git clone https://github.com/themakerrobot/x-openpibo.git
      cd x-openpibo
      sudo python3 setup.py install
      
      # 또는
      
      sudo pip3 install git+https://github.com/themakerrobot/x-openpibo
      ```

   - 추가 도구 설치

      ```bash
      # 샘플 데이터
      git clone https://github.com/themakerrobot/x-openpibo-data.git
      
      # 예제 코드
      git clone https://github.com/themakerrobot/x-openpibo-example.git
      
      # 각종 툴
      git clone https://github.com/themakerrobot/x-openpibo-tools.git
      ```

8. [카카오 api키를 발급받습니다.](http://https://themakerrobot.github.io/x-openpibo/docs/build/html/notes/kakao_api.html)