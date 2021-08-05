from setuptools import setup, find_packages

setup(
    name='openpibo',
    version='1.0.0',
    description='Openpibo libraries',
    url='https://github.com/themakerrobot/openpibo-ex',
    author='Circulus',
    author_email='hojp7874@circul.us',
    license='Circulus',
    packages=find_packages(exclude=[]),
    python_requires= '>=3',
    install_requires=[
        'opencv-python==4.1.0.25',
        'opencv-contrib-python==4.1.0.25',
        'dlib==19.19.0',
        'pyzbar==0.1.8',
        'pytesseract==0.3.4',
        'beautifulsoup4==4.6.0',
        'konlpy==0.5.2',
        'future==0.18.2',
        'google_trans_new==1.1.9',
        'pillow==7.2.0',
        'RPi.gpio==0.7.0',
        'pyserial==3.5',
        'requests==2.25.1',
        'pytest==6.2.4',
    ]
)