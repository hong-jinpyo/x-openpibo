"""
Kakao 음성 API를 사용하여 PIBO에 장착되어 있는 마이크와 스피커를 통해 사람의 음성 언어를 인식하거나 합성할 수 있습니다.
"""

import csv
import random
#import io
import json
import os
from konlpy.tag import Mecab
import requests
from .modules.speech.google_trans_new import google_translator
from . import config
#from google.cloud import speech
#from google.cloud.speech import enums
#from google.cloud.speech import types
current_path = os.path.dirname(os.path.realpath(__file__))


def getDiff(aT, bT):
  """
  (``get_dialog`` 메서드의 내부함수)

  ``get_dialog`` 의 과정 중 사용자의 질문과 유사한 데이터를 찾는 함수입니다.
  """

  cnt = 0
  for i in aT:
    for j in bT:
      if i == j:
        cnt += 1
  return cnt / len(aT)

class Speech:
  """
  파이보에서 말과 관련된 자연어처리 기능을 하는 클래스 입니다.

  * 번역 (한국어, 영어)
  * TTS (Text to Speech)
  * STT (Speech to Text)

  ``config.json`` 의 KAKAO_ACCOUNT에 본인의 ``KAKAO REST API KEY`` 를 입력해야 사용할 수 있습니다.

  example::

    pibo_speech = Speech()
  """

  def __init__(self):
    self.translator = google_translator()
    self.kakao_account = config['KAKAO_ACCOUNT']

  def translate(self, string, to='ko'):
    """
    구글 번역기를 이용해서 문장을 번역합니다.

    example::

      pibo_speech.translate('안녕하세요! 만나서 정말 반가워요!', to='ko')
      # "Hello! I'm really happy to meet you!"

    :param str string: 번역할 문장

    :param str to: 번역될 언어

      ``en`` 또는 ``ko``
    """

    '''curl -v -X POST "https://dapi.kakao.com/v2/translation/translate" \
    -d "src_lang=kr" \
    -d "target_lang=en" \
    --data-urlencode "query=지난해 3월 오픈한 카카오톡 주문하기는 현재까지 약 250만명의 회원을 확보했으며, 주문 가능한 프랜차이즈 브랜드는 38개, 가맹점수는 약 1만 5천여곳에 달한다. 전 국민에게 친숙한 카카오톡 UI를 활용하기 때문에 남녀노소 누구나 쉽게 이용할 수 있으며, 별도의 앱을 설치할 필요 없이 카카오톡 내에서 모든 과정이 이뤄지는 것이 특징이다. 지난해 9월 업계 최초로 날짜와 시간을 예약한 뒤 설정한 매장에서 주문 음식을 찾아가는 ‘픽업’ 기능을 도입했고, 올해 1월 스마트스피커 ‘카카오미니’에서 음성을 통해 주문 가능한 메뉴를 안내받을 수 있도록 서비스를 연동하며 차별화를 꾀했다. 중소사업자들이 카카오톡 주문하기에 입점하게 되면 4,300만 카카오톡 이용자들과의 접점을 확보하고, 간편한 주문 과정으로 만족도를 높일 수 있게 된다. 카카오톡 메시지를 통해 신메뉴 출시, 프로모션 등의 소식을 전달할 수 있고, 일대일 채팅 기능을 적용하면 고객과 직접 상담도 가능하다." \
    -H "Authorization: KakaoAK {REST_API_KEY}"'''

    '''
    # kakao translate source
    url = 'https://dapi.kakao.com/v2/translation/translate'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'KakaoAK ' + self.kakao_account
    }

    res = requests.post(url, headers=headers, data={"src_lang":"kr", "target_lang":"en", "query":string})
    try:
      result = {"result":True, "value":json.loads(res.text)["translated_text"]}

    except Exception as ex:
      result = {"result":False, "value":""}
    return result['value']'''
    return self.translator.translate(string, lang_tgt=to)

  def tts(self, string, filename="tts.mp3"):
    """
    TTS(Speech to Speech)
    
    Speech(문자)를 Speech(말)로 변환합니다.

    example::

      pibo_speech.tts('안녕하세요! 만나서 반가워요!', '/home/pi/.../tts.mp3')
    
    :param str string: 변환할 문구

    :param str filename: 변환된 음성파일의 경로
    """

    '''curl -v "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize" \
    -H "Content-Type: application/xml" \
    -H "Authorization: KakaoAK API_KEY" \
    -d '<speak> 그는 그렇게 말했습니다.
    <voice name="MAN_DIALOG_BRIGHT">잘 지냈어? 나도 잘 지냈어.</voice>
    <voice name="WOMAN_DIALOG_BRIGHT" speechStyle="SS_ALT_FAST_1">금요일이 좋아요.</voice> </speak>' > result.mp3'''

    url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
    headers = {
      'Content-Type': 'application/xml',
      'Authorization': 'KakaoAK ' + self.kakao_account
    }
    r = requests.post(url, headers=headers, data=string.encode('utf-8'))
    with open(filename, 'wb') as f:
      f.write(r.content)

  def stt(self, filename="stream.wav", timeout=5):
    """
    STT(Speech to Speech)
    
    Speech(말)을 Speech(문자)로 변환합니다.

    ``timeout`` 초 동안 녹음 후 ``filename`` 의 이름으로 저장하고, 이를 텍스트변환하여 출력합니다.

    example::

      pibo_speech.stt('/home/pi/.../stream.wav', 5)

    :param str filename: 저장할 파일 이름

    :param int timeout: 녹음할 시간(s)
  
    :returns: ``True`` / ``False``
    """

    cmd = "arecord -D dmic_sv -c2 -r 16000 -f S32_LE -d {} -t wav -q -vv -V streo stream.raw;sox stream.raw -c 1 -b 16 stream.wav;rm stream.raw".format(timeout)
    os.system(cmd)

    '''curl -v "https://kakaoi-newtone-openapi.kakao.com/v1/recognize" \
    -H "Transfer-Encoding: chunked" -H "Content-Type: application/octet-stream" \
    -H "Authorization: KakaoAK API_KEY" \
    --data-binary @stream.wav '''

    url = 'https://kakaoi-newtone-openapi.kakao.com/v1/recognize'
    headers = {
      'Content-Type': 'application/octet-stream',
      'Authorization': 'KakaoAK ' + self.kakao_account
    }

    data = open(filename, 'rb').read()
    res = requests.post(url, headers=headers, data=data)
    try:
      result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
    except Exception as ex:
      result_json_string = res.text[res.text.index('{"type":"errorCalled"'):res.text.rindex('}')+1]
    result = json.loads(result_json_string)
    return result['value']

class Dialog:
  """
  파이보에서 대화와 관련된 자연어처리 기능을 하는 클래스입니다.

  * 형태소 및 명사 분석
  * 챗봇 기능

  example::

    pibo_dialog = Dialog()
  """

  def __init__(self):
    self.dialog_path = current_path+"/data/models/dialog.csv"
    self.mecab = Mecab()
    self.dialog_db = []
    with open(self.dialog_path, 'r', encoding='utf-8') as f:
      rdr = csv.reader(f)
      self.dialog_db = [[self.mecab_morphs(line[0]), line[1], line[2]]for line in rdr]

  def mecab_pos(self, string):
    """
    형태소를 품사와 함께 추출합니다.

    exmaple::

      pibo_dialog.mecab_pos('아버지가 방에 들어가셨다.')
      # [('아버지', 'NNG'), ('가', 'JKS'), ('방', 'NNG'), ('에', 'JKB'), ('들어가', 'VV'), ('셨', 'EP+EP'), ('다', 'EF'), ('.', 'SF')]
    
    :param str string: 분석할 문장 (한글)

    :returns: 분석한 결과

      ``list`` 타입 입니다.
    """

    return self.mecab.pos(string)

  def mecab_morphs(self, string):

    """
    형태소를 추출합니다.

    exmaple::

      pibo_dialog.mecab_morphs('아버지가 방에 들어가셨다.')
      # ['아버지', '가', '방', '에', '들어가', '셨', '다', '.']
    
    :param str string: 분석할 문장 (한글)

    :returns: 분석한 결과

      ``list`` 타입 입니다.
    """

    return self.mecab.morphs(string)

  def mecab_nouns(self, string):

    """
    명사를 추출합니다.

    exmaple::

      pibo_dialog.mecab_nouns('아버지가 방에 들어가셨다.')
      # ['아버지', '방']
    
    :param str string: 분석할 문장 (한글)

    :returns: 분석한 결과

      ``list`` 타입 입니다.
    """
    return self.mecab.nouns(string)

  def get_dialog(self, q):
    """
    일상대화에 대한 답을 추출합니다.

    저장된 데이터로부터 사용자의 질문과 가장 유사한 질문을 선택해 그에 대한 답을 출력합니다.

    해당 데이터를 수정하기 위해서는, openpibo 패키지를 clone 하여 설치하여야 합니다::

      git clone https://github.com/themakerrobot/x-openpibo.git
      cd x-openpibo
      sudo python3 setup.py install

    이후 다음 경로로 저장된 데이터를 수정합니다::

      # x-openpibo를 clone 한 경로로부터,
      x-openpibo/openpibo/data/models/dialog.csv

    example::

      pibo_dialog.get_dialog('나랑 같이 놀자')
      # '지금 그러고 있어요.'
    """

    max_acc = 0
    max_ans = []
    c = self.mecab_morphs(q)
    for line in self.dialog_db:
      acc = getDiff(line[0], c)

      if acc == max_acc:
        max_ans.append(line)

      if acc > max_acc:
        max_acc = acc
        max_ans = [line]

    return random.choice(max_ans)[1]
