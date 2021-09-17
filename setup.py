import os, json

if os.path.isfile('/home/pi/config.json') == False:
  with open('/home/pi/config.json', 'w') as f:
    json.dump({"DATA_PATH":"/home/pi/openpibo-files/data", "KAKAO_ACCOUNT":"", "robotId":""}, f)


from setuptools import setup, find_packages
from openpibo import __version__ as VERSION

setup(
    name                        = 'openpibo',
    version                     = VERSION,
    packages                    = find_packages(),
    package_data                = {'' : ['data/models/*']},
    include_package_data        = True,
    zip_safe                    = False,
    python_requires             = '>=3',
    install_requires            = [
        'opencv-python==4.1.0.25',
        'opencv-contrib-python==4.1.0.25',
        'dlib==19.19.0',
        'pyzbar==0.1.8',
        'pytesseract==0.3.4',
        'beautifulsoup4==4.6.0',
        'konlpy==0.5.2',
        'future==0.18.2',
        'pillow==7.2.0',
        'RPi.gpio==0.7.0',
        'pyserial==3.5',
        'requests==2.25.1',
        'pytest==6.2.4',
        'rich==10.6.0',
        'flask==2.0.1',
        'flask-socketio==5.1.1',
    ]
)
