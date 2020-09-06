import requests
from bs4 import BeautifulSoup
search_name = '숭례문'
url_list = 'http://www.cha.go.kr/cha/SearchKindOpenapiList.do?pageUnit=30&ccbaMnm1=' + search_name
# url_search = 'http://www.cha.go.kr/cha/SearchKindOpenapiDt.do?ccbaCtcd=21&ccbaAsno=00&ccbaCtcd=11'
# ccbaKdcd 종목코드, ccbaAsno 지정번호, ccbaCtcd 시도코드
html = requests.get(url_list)


sp_html = html.text.split('<sn>')
searched_list = []
for heritage in sp_html:
    temp_html = BeautifulSoup(heritage, 'html.parser')
    try:
        temp_dict = {}
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

print('검색어 : ', search_name)
print('몇개임? : ', len(searched_list))
for i in searched_list:
    print(i)

# print(searched_list)
# print(html.text)

# parsed_html = BeautifulSoup(html.text, 'html.parser')

# print(sp_html)

# print('이름 1 : ', parsed_html.ccbamnm1.text)
# print('이름 2 : ', parsed_html.ccbamnm2.text)
# print('위치 : ', parsed_html.ccbactcdnm.text, parsed_html.ccsiname.text)
# print('경도 : ', parsed_html.longitude.text, ', 위도 : ', parsed_html.latitude.text)
