# Cultural_Heritage_Administration_API
## 문화재청 Open API 사용
<hr>
#### LikeLion 8th hackathon 출품 예정작 `공아역`에 사용

- 사용자의 검색에 맞는 문화재 이미지 및 정보 출력을 위함

<hr>

### 20.09.06 기준

```python
import requests
search_name = '숭례문'
url_list = 'http://www.cha.go.kr/cha/SearchKindOpenapiList.do?pageUnit=30&ccbaMnm1=' + search_name

html = requests.get(url_list)
```

- requests를 사용하여 api 호출
- 문화재청 api는 별도의 key가 존재하지 않음
- ccbaMnm1은 문화재의 이름, 예를 들기 위하여 '숭례문'으로 설정
  <i>이름을 기준으로 문화재 검색을 위함</i>
- pageUnit은 한 페이지에 보여줄 문화재의 수, 30으로 설정
  <i>검색 결과에 해당하는 모든 문화재를 보여주기 위해 api를 여러번 호출하는 방법 대신 적당히 보여준 후 사용자의 자세한 검색 유도</i>

```python
sp_html = html.text.split('<sn>')
```
- 호출한 값(html 형식)을 순번 태그인 `<sn>`을 기준으로 `split`함

```python
# 딕셔너리들이 들어갈 리스트
searched_list = []
for heritage in sp_html:
    # split된 값들을 bs를 사용하여 parsing
    temp_html = BeautifulSoup(heritage, 'html.parser')

    # 태그들이 없는 html 선언부분등을 예외처리
    try:
        # 빈 딕셔너리 생성
        temp_dict = {}
        # 각 정보에 해당하는 key와 value 넣어줌
        temp_dict['문화재명1'] = temp_html.ccbamnm1.text
        temp_dict['문화재명2'] = temp_html.ccbamnm2.text
        temp_dict['위치_도'] = temp_html.ccbactcdnm.text
        temp_dict['위치_시'] = temp_html.ccsiname.text
        temp_dict['종목코드'] = temp_html.ccbakdcd.text
        temp_dict['시도코드'] = temp_html.ccbactcd.text
        temp_dict['지정번호'] = temp_html.ccbaasno.text
        searched_list.append(temp_dict)
    except:
        pass
```
- split된 html 내용을 기준으로 for문 수행
- 각 값들을 `BeautifulSoup`을 사용하여 `parsing`
- 필요한 내용의 이름과 값을 각 딕셔너리의 key와 value로 저장한 후 `searched_list`에 추가
- `sp_html`에 head 태그와 같이 필요한 태그들이 존재하지 않은 요소들이 있기 때문에 `try`, `except`를 사용하여 예외처리
