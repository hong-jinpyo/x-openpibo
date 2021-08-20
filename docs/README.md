문서화 진행중...

sphinx로 제작한 문서

sphinx pip requirements
```
sphinx==4.1.2
myst_parser==0.15.1
```

문서 만들기:

```
# ~/x-openpibo
sphinx-apidoc -f -o docs/source openpibo/ --separate

cd docs
make html
```
만약 error 발생 시 다음 명령어로 sphinx 재설치
```
sudo apt-get install python3-sphinx
```

이후 `~/x-openpibo/docs/index.html` 실행

테마 바꾸기:

해당 레퍼런스 참고

[스핑크스 테마 링크](https://sphinx-themes.org/)