file = open("./data/phone_and_table/smart_phone.csv","r",encoding='utf-8')
file2 = open("data.csv","w",encoding='utf-8')

for line in file:
    arr_words = line.split(',')
    print(arr_words)
    break
        


