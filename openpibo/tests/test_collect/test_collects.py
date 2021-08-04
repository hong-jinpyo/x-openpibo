import sys
sys.path.append('../..')
from utils.config import Config as cfg

sys.path.append(cfg.OPENPIBO_PATH+'/lib')
from collect import *

wiki = Namuwiki('강아지')
print(wiki)

weather = Weather('서울')
print(weather)

news = News()
print(news)