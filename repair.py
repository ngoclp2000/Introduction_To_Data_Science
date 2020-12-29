import string
import re
file = open("./data/laptop/Laptop.csv","r",encoding='utf-8')
file2 = open("data.csv","w",encoding='utf-8')
count = 0

for line in file:
    if count == 0:
        file2.write(line)
        count +=1
        continue
    j = 0
    arr_words = line.split(',')
    index = 7
    if arr_words[index]!= 'None' and arr_words[index] != 'Đang cập nhật' and arr_words[index] != '':
        x = re.findall("[0-9]+",arr_words[index])
        if len(x) != 0:
            arr_words[index] = x[0]
    # if arr_words[4] != 'None' and arr_words[4] != 'Đang cập nhật' and arr_words[4] != '':
    #     x = re.findall("[0-9]+",arr_words[4])
    #     if len(x) != 0:
    #         y = float(x[0])
    #         if y > 100:
    #             y /= 1000
    #         else:
    #             y /= 10
    #         arr_words[4] = str(y)
    
    for word in arr_words:
        j+=1
        file2.write(word)
        if j != len(arr_words):
            file2.write(',')


    



