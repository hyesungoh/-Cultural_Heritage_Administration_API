import requests
from bs4 import BeautifulSoup
# search_name = '숭례문'
search_name = '화성'
# search_name = input()

# 파일 생성
f = open("heritage.txt", 'a')


# url_list = 'http://www.cha.go.kr/cha/SearchKindOpenapiList.do?pageUnit=3&ccbaMnm1=' + search_name
url_list = 'http://www.cha.go.kr/cha/SearchKindOpenapiList.do?pageUnit=15944'
# url_search = 'http://www.cha.go.kr/cha/SearchKindOpenapiDt.do?ccbaCtcd=21&ccbaAsno=00&ccbaCtcd=11'
# ccbaKdcd 종목코드, ccbaAsno 지정번호, ccbaCtcd 시도코드
html = requests.get(url_list)

# print(html.text)
sp_html = html.text.split('<sn>')
searched_list = []

progress = 1
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
        temp_dict['시대'] = parsed_detail.cccename.text
        temp_dict['경도'] = parsed_detail.longitude.text
        temp_dict['위도'] = parsed_detail.latitude.text
        searched_list.append(temp_dict)

        print('현재 진행상황 : ', progress)
        progress += 1
    except:
        pass

print('검색어 : ', search_name)
print('몇개임? : ', len(searched_list))

for i in searched_list:
    for key, value in i.items():
        txt_data = key + ':' + value + '\n'
        print(txt_data)
        # f.write(txt_data)

f.write(str(searched_list))
f.close()

# print('\n\n이렇게 들어가 있음 : \n', searched_list[0])


# print(searched_list)
# print(html.text)

# parsed_html = BeautifulSoup(html.text, 'html.parser')

# print(sp_html)

# print('이름 1 : ', parsed_html.ccbamnm1.text)
# print('이름 2 : ', parsed_html.ccbamnm2.text)
# print('위치 : ', parsed_html.ccbactcdnm.text, parsed_html.ccsiname.text)
# print('경도 : ', parsed_html.longitude.text, ', 위도 : ', parsed_html.latitude.text)
