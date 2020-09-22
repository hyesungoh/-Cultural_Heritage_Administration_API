heritage_txt = open("heritage.txt", 'r')

heritage_list = []
i = 0
while True:
    line = heritage_txt.readline()
    if not line: break
    heritage_list.append(eval(line))

    i += 1
    if i % 100 == 0: print(i, "/ 19544")

# eval 테스
# for _ in range(5):
#     line = heritage_txt.readline()
#     heritage_list.append(eval(line))

print(heritage_list[0]['문화재명1'])
print('총 문화재 수 : ', len(heritage_list))
heritage_txt.close()

