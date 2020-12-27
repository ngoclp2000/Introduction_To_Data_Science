file = open("./data/phone_and_table/Maytinhbang.csv","r",encoding='utf-8')
file2 = open("data.csv","w",encoding='utf-8')

for line in file:
    arr_words = line.split(',')
    count = 9999999
    string = ""
    for i in range(len(arr_words)):
        if i == 0:
            string += str( arr_words[i])
            string += ","
        elif i > count:
            string += arr_words[i]
            if i != len(arr_words) -1:
                string += ','
        elif "₫" not in arr_words[i]:
            string += arr_words[i]
            string += ' '
        elif "₫" in arr_words[i]:
            string += ','
            string += arr_words[i]
            string += ','
            count = i
        
    file2.write(string)
        


