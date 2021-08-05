import json
with open('/home/pi/config.json', 'r') as f:
    _cfg = json.load(f)
    kakao_account = _cfg['KAKAO_ACCOUNT']
    data_path = _cfg['OPENPIBO_DATA_PATH']