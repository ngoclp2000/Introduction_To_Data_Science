file = open("test.csv","r",encoding='utf-8')
file2 = open("data.csv","w",encoding='utf-8')

for line in file:
    arr_words = line.split(',')
    for i in range(len(arr_words)):
        if i < 4:
            file2.write(arr_words[i])
            file2.write(',')
        else:
            file2.write(arr_words[i])
            if i != len(arr_words) -1:
                file2.write(' ')
