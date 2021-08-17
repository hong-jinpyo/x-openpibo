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
이후 `~/x-openpibo/docs/index.html` 실행