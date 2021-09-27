# collect

## collect_test.py

각종 데이터를 수집해옵니다.

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

**collect_test.py 결과**

다음 텍스트가 출력됩니다.

```
강아지 (dog)는 개의 새끼를 일컫는다.[1] 강아지는 성체로 발달하는 과정에 있으므로 자라면서 털색이나 체형 등이 달라질 수 있으며[2], 정서적인 변화를 겪기도 한다.[3]

내일 오후부터 모레까지 가끔 비, 내일 낮까지 산발적 약한 비 또는 빗방울 곳
다음 달부터 '카드 캐시백'…백화점 안 되고 할부 가능
```