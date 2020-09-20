# Cultural_Heritage_Administration_API
## 문화재청 Open API 사용
<hr>
#### LikeLion 8th hackathon 출품 예정작 '공아역'에 사용

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


### 20.09.08 기준

```python
for heritage in sp_html:
    temp_html = BeautifulSoup(heritage, 'html.parser')
    try:
        temp_dict = {}
        temp_dict['문화재명1'] = temp_html.ccbamnm1.text
        temp_dict['문화재명2'] = temp_html.ccbamnm2.text
        temp_dict['위치_도'] = temp_html.ccbactcdnm.text
        temp_dict['위치_시'] = temp_html.ccsiname.text

        temp_kbcd = temp_html.ccbakdcd.text
        temp_dict['종목코드'] = temp_kbcd

        temp_ctcd = temp_html.ccbactcd.text
        temp_dict['시도코드'] = temp_ctcd

        temp_anno = temp_html.ccbaasno.text
        temp_dict['지정번호'] = temp_anno

        temp_require = 'ccbaKdcd=' + temp_kbcd + '&ccbaCtcd=' + temp_ctcd + '&ccbaAsno=' + temp_anno

        # img_url = 'http://www.cha.go.kr/cha/SearchImageOpenapi.do?' + temp_require
        # img = requests.get(img_url)
        # sp_img = img.text.split('<sn>')
        # parsed_img = BeautifulSoup(sp_img[1], 'html.parser')
        # temp_dict['이미지'] = parsed_img.imageurl.text

        detail_url = 'http://www.cha.go.kr/cha/SearchKindOpenapiDt.do?' + temp_require

        detail = requests.get(detail_url)
        parsed_detail = BeautifulSoup(detail.text, 'html.parser')
        temp_dict['이미지'] = parsed_detail.imageurl.text
        temp_dict['내용'] = parsed_detail.content.text


        searched_list.append(temp_dict)
    except:
        pass
```

- 문화재 이미지 검색 api와 문화재 상세정보 api를 둘 다 호출하지 않고 문화재 상세정보에 있는 대표 이미지를 사용
- 상세정보 검색에 필요한 종목, 지정, 시도 코드를 변수로 지정 > url 요첨에 필요한 문자열을 변수로 지정
- 문화재 검색과 같이 requests, BeautifulSoup를 사용
- <i>문화재 리스트에 존재하는 문화재 마다 api를 호출하여 시간이 오래걸리는 이슈가 있음, 어떻게 해결해야 될까?</i>


#### 20.09.14 기준
- 문화재청 API에 총 15935개의 정보가 있음 > 검색마다 API를 호출하는 건 상당히 비효율 적이라고 생각 > 개발 환경에서 model에 저장 후 필요한 정보를 불러오는 방법을 사용해야겠음 > 장고 프로젝트에서 모델을 만들어야 함 > 기존 슬라이싱 및 파싱한 것을 토대로 모델에 저장 > 15000여개의 데이터를 모델에 저장하면서 경과치를 볼 수 있을까?

#### 20.09.15 기준
- 장고 모델에 15000여개의 데이터를 저장 > 검색은 `filter`을 이용하여 구현할 예정

#### 20.09.18 기준
- 모델 저장 페이지에서 api를 호출하여 저장하는 방법 대신, 로컬에서 api에서 필요한 정보를 뺀 파일을 만들어 그것을 이용하여 저장하는 방법을 사용할 예정

#### 20.09.19 기준
```python
f = open("heritage.txt", 'a')

... 중략

for i in searched_list:
    for key, value in i.items():
        txt_data = key + ':' + value
        f.write(txt_data)
f.close()
```
- 파일 입출력을 이용하여 key와 value를 :로 나누어 저장, 이제 15000여개의 모델을 저장하면서 진행상황을 어떻게 볼지 고민중

#### 20.09.20 기준
```python
url_list = 'http://www.cha.go.kr/cha/SearchKindOpenapiList.do?pageUnit=15944'
```
- api에서 가져올 요소의 수를 api에 존재하는 모든 문화재 수인 19544로 설정
```python
progress = 1
for heritage in sp_html:
    temp_html = BeautifulSoup(heritage, 'html.parser')
    try:
        temp_dict = {}
        temp_dict['문화재명1'] = temp_html.ccbamnm1.text
        ... 중략
        print('현재 진행상황 : ', progress)
        progress += 1
    except:
        pass
```
- 반복문에 출력문을 넣어 경과정도를 확인할 수 있게 함
```python
f.write(str(searched_list))
```
- 딕셔너리 자료형들로 이루어진 리스트를 문자열화하여 파일에 입력
