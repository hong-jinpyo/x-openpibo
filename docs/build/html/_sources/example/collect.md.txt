# Collect

## collect_test.py

> 각종 데이터를 수집해옵니다.

```python
from openpibo.collect import *

# 위키피디아 스크래핑
wiki = Wikipedia()
wiki.search('강아지')
print(wiki) # 강아지에 대한 설명 출력

# 날씨 데이터 가져오기
weather = Weather()
weather.search('서울')
print(weather) # 서울 날씨 출력

# 뉴스 가져오기
news = News()
news.search('경제')
print(news) # 경제 뉴스 출력
```

**collect_test.py 실행**

```shell
pi@raspberrypi:~/openpibo-examples/collect $ sudo python3 collect_test.py
```
