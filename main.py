from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import re
import numpy as np
import string
import unidecode
PATH = "/Users/nguyentuandung/Desktop/Data Science/ngoc/chromedriver"

driver = webdriver.Chrome(PATH)
urls = [
    'https://tiki.vn/dien-tu-dien-lanh/c4221',
]
def clean_string(string): 
    string = string.replace('\n',' ')
    string = string.replace(',',' ')
    string = string.rstrip()
    string_without_newline = ""
    for c in string:
        if c.isalpha() or c.isdigit() or c == ' ':
            string_without_newline += c
    return string_without_newline

def click_next_button():
    return driver.execute_script('''
                    let t1 = document.querySelector('i[style="transform: rotate(180deg);"]');
                    let t2 = document.querySelector('i[style="transform:rotate(180deg)"]');
                    let t3 = document.querySelector('i[style="transform:rotate(180deg);"]');
                    let t4 = document.querySelector('i[style="transform: rotate(180deg)"]');
                    if (t1 != null){
                        t1.click();
                        return 1;
                    }else if(t2 != null){
                        t2.click();
                        return 1;
                    }else if (t3 != null){
                        t3.click();
                        return 1;
                    }else if(t4 != null){
                        t4.click();
                        return 1;
                    }
                    return 0;
            ''')
def _check_button_next():
    return driver.execute_script('''
            let t1 = document.querySelector('i[style="transform: rotate(180deg);"]');
            let t2 = document.querySelector('i[style="transform:rotate(180deg)"]');
            let t3 = document.querySelector('i[style="transform:rotate(180deg);"]');
            let t4 = document.querySelector('i[style="transform: rotate(180deg)"]');
            if (t1 != null || t2 != null || t3 != null || t4 != null){
                        return 1;
            }else return 0;
        ''')
def check_sub_category():
    return driver.execute_script('''
            let x = document.querySelectorAll('a[class="item item--category "]');
            if (x.length == 0)
                return 0
            else return 1;
    ''')
def check_next_button_comments():
    return driver.execute_script(''' 
                    let element = document.querySelector('a[class="btn next"]');
                    if( element != null){
                        return 1;
                    }else return 0;

    ''')
def get_comments():
    return driver.execute_script('''
        cells = document.querySelectorAll('.review-comment__content');
        auto_comment = document.querySelectorAll('.review-comment__title');
        let count = 0;
        cms = [];
        [].forEach.call(cells, function (el) {
            if(el.textContent != '' ){
                cms.push(el.textContent);
            }else{
                cms.push(auto_comment[count].textContent);
            }
            count += 1;
        });
        return cms
    ''')
def get_info(cate_name,count):
    name = driver.find_elements_by_xpath(
                            '//div[@class="name"]/span')[count].text
    price = driver.find_elements_by_xpath(
                            '//div[@class="price-discount__price"]')[count].text
    price = price.replace('.','')
    price = price.replace('₫','')
    driver.get(products[count].get_attribute("href"))
    time.sleep(1)
    driver.execute_script(
        "document.querySelectorAll('.group')[1].scrollIntoView()")
    number_of_comment = driver.execute_script('''
                        let ele =  document.querySelector('a[class="number"]');
                        if (ele != null){
                            return ele.text;
                        }else return 0;
                        ''')
                        
    print("Before regrex: "+ str(number_of_comment)) 
    if(number_of_comment != 0) :
        number_of_comment = re.findall("[0-9]+", number_of_comment)[0]
    if int(number_of_comment) > 500:
        number_of_comment = 500
    data = [name,price,number_of_comment]
    if cate_name == "Máy giặt":
        description = driver.execute_script('''
            let check = 0;
            let rs = []
            let cells = document.querySelectorAll('td');
            for(let i = 0 ; i < cells.length ;i++){
                if(cells[i].textContent == "Thương hiệu"){
                    rs.push(cells[++i].textContent)
                    check = 1;
                }
            }
            if(check == 0){
                rs.push("Node");
            }else{
                check = 0;
            }
            for(let i = 0 ; i < cells.length ;i++){
                if(cells[i].textContent == "Kích thước"){
                    rs.push(cells[++i].textContent)
                    check = 1;
                }
            }
            if(check == 0){
                rs.push("Node");
            }else{
                check = 0;
            }
            for(let i = 0 ; i < cells.length ;i++){
                if(cells[i].textContent == "Kiểu máy giặt"){
                    rs.push(cells[++i].textContent)
                    check = 1;
                }
            }
            if(check == 0){
                rs.push("Node");
            }else{
                check = 0;
            }
            for(let i = 0 ; i < cells.length ;i++){
                if(cells[i].textContent == "Trọng lượng"){
                    rs.push(cells[++i].textContent)
                    check = 1;
                }
            }
            if(check == 0){
                rs.push("Node");
            }else{
                check = 0;
            }
            return rs;
        ''')
        for word in description:
            data.append(clean_string(word))
    elif cate_name == "Tivi":
        description = driver.execute_script('''
            let check = 0;
            let rs = []
            let cells = document.querySelectorAll('td');
            for(let i = 0 ; i < cells.length ;i++){
                if(cells[i].textContent == "Thương hiệu"){
                    rs.push(cells[++i].textContent)
                    check = 1;
                }
            }
            if(check == 0){
                rs.push("None");
            }else{
                check = 0;
            }
            for(let i = 0 ; i < cells.length ;i++){
                if(cells[i].textContent == "Kích thước màn hình"){
                    rs.push(cells[++i].textContent)
                    check = 1;
                }
            }
            if(check == 0){
                rs.push("None");
            }else{
                check = 0;
            }
            for(let i = 0 ; i < cells.length ;i++){
                if(cells[i].textContent == "Độ phân giải"){
                    rs.push(cells[++i].textContent)
                    check = 1;
                }
            }
            if(check == 0){
                rs.push("None");
            }else{
                check = 0;
            }
            for(let i = 0 ; i < cells.length ;i++){
                if(cells[i].textContent == "Loại Tivi"){
                    rs.push(cells[++i].textContent)
                    check = 1;
                }
            }
            if(check == 0){
                rs.push("None");
            }else{
                check = 0;
            }
            for(let i = 0 ; i < cells.length ;i++){
                if(cells[i].textContent == "Khối lượng có chân"){
                    rs.push(cells[++i].textContent)
                    check = 1;
                }
            }
            if(check == 0){
                rs.push("None");
            }else{
                check = 0;
            }
            return rs;
        ''')
        c = 0
        for word in description:
            if c == 1 or c == 4:
                word = clean_string(word)
                number = re.findall("[0-9]+", word)
                if len(number) != 0:
                    data.append(number[0])
                else:
                    data.append(word)
            else:
                data.append(clean_string(word))
            c+=1
    time.sleep(1)
    return data
for url in urls:
    
    count_cate = 0
    driver.get(url)
    time.sleep(1)
    categories = driver.find_elements_by_xpath('//a[@class="item item--category "]')
    while count_cate < len(categories) and categories[count_cate] is not None:
        count_sub_cate = 0
        cat_text = categories[count_cate].text
        if "Tivi" != cat_text:
            count_cate += 1
            continue
        cat_href = categories[count_cate].get_attribute("href")
        time.sleep(1)
        driver.get(cat_href)
        driver.execute_script('''
            document.querySelectorAll('a[data-view-id="search_sort_item"]')[1].click()
        ''')
        time.sleep(1)
        check_sub_categories =  check_sub_category()
        print(check_sub_categories)
        if check_sub_categories == 1 and cat_text != "Tivi":
            index = 0
            sub_categories = driver.find_elements_by_xpath('//a[@class="item item--category "]')
            while count_sub_cate < len(sub_categories) and sub_categories[count_sub_cate] is not None:
                filename = unidecode.unidecode(sub_categories[count_sub_cate].text)
                arr_words = filename.split(' ')
                filename_normal_form = ""
                for word in arr_words:
                    filename_normal_form += word
                filename_normal_form = ".\data\electric_device\\" + filename_normal_form + ".csv"
                file = open(filename_normal_form,"a",encoding='utf-8')
                driver.get(sub_category.get_attribute("href"))
                driver.execute_script('''
            document.querySelectorAll('a[data-view-id="search_sort_item"]')[1].click()
        ''')
                check_button_next = _check_button_next()
                if check_button_next == 1:
                    while check_button_next == 1:
                        count = 0
                        products = driver.find_elements_by_xpath('//a[@class="product-item"]')
                        print(len(products))
                        while count < len(products) and products[count] is not None:
                            number_of_comment_count = 0
                            infos = get_info(cat_text,count)
                            #time.sleep(1)
                            check = check_next_button_comments()
                            element_product = []
                            if(check == 1):
                                while check == 1 and number_of_comment_count <= 500:
                                    results = get_comments()
                                    number_of_comment_count += len(results)
                                    time.sleep(0.5)
                                    check = check_next_button_comments()
                                    if check == 1:
                                        driver.execute_script(''' 
                                            document.querySelector('a[class="btn next"]').click();
                                        ''')
                                    for result in results:
                                        string_without_newline = clean_string(result)
                                        string_push = ""
                                        string_push += str(index) + ','
                                        for info in infos:
                                            print(info)
                                            string_push += str(info) + ','
                                        string_push += string_without_newline + '\n'
                                        file.write(string_push)
                                    if number_of_comment_count == 0:
                                        string_push = ""
                                        string_push += str(index) + ','
                                        for info in infos:
                                            string_push += str(info) + ','
                                        string_push += "None" + '\n'
                                        file.write(string_push)
                            else:
                                results = get_comments()
                                number_of_comment_count += len(results)
                                #time.sleep(1)
                                for result in results:
                                    string_without_newline = clean_string(result)
                                    string_push = ""
                                    string_push += str(index) + ','
                                    for info in infos:
                                        string_push += str(info) + ','
                                    string_push += string_without_newline + '\n'
                                    file.write(string_push)
                                if number_of_comment_count == 0:
                                    string_push = ""
                                    string_push += str(index) + ','
                                    for info in infos:
                                        string_push += str(info) + ','
                                    string_push += "None" + '\n'
                                    file.write(string_push)
                            count += 1
                            index += 1
                            driver.back()
                            time.sleep(1)
                            products = driver.find_elements_by_xpath('//a[@class="product-item"]')
                        check_button_next = click_next_button()
                        time.sleep(1)
                else:
                    count = 0
                    products = driver.find_elements_by_xpath('//a[@class="product-item"]')
                    print(len(products))
                    while count < len(products) and products[count] is not None:
                        number_of_comment_count = 0
                        infos = get_info(cat_text,count)
                        #time.sleep(1)
                        check = check_next_button_comments()
                        element_product = []
                        if(check == 1):
                            while check == 1 and number_of_comment_count <= 500:
                                results = get_comments()
                                number_of_comment_count += len(results)
                                time.sleep(0.5)
                                check = check_next_button_comments()
                                if check == 1:
                                    driver.execute_script(''' 
                                            document.querySelector('a[class="btn next"]').click();
                                    ''')
                                for result in results:
                                    string_without_newline = clean_string(result)
                                    string_push = ""
                                    string_push += str(index) + ','
                                    for info in infos:
                                        print(info)
                                        string_push += str(info) + ','
                                    string_push += string_without_newline + '\n'
                                    file.write(string_push)
                                if number_of_comment_count == 0:
                                    string_push = ""
                                    string_push += str(index) + ','
                                    for info in infos:
                                        string_push += str(info) + ','
                                    string_push += "None" + '\n'
                                    file.write(string_push)
                        else:
                            results = get_comments()
                            number_of_comment_count += len(results)
                                #time.sleep(1)
                            for result in results:
                                string_without_newline = clean_string(result)
                                string_push = ""
                                string_push += str(index) + ','
                                for info in infos:
                                    string_push += str(info) + ','
                                string_push += string_without_newline + '\n'
                                file.write(string_push)
                            if number_of_comment_count == 0:
                                string_push = ""
                                string_push += str(index) + ','
                                for info in infos:
                                    string_push += str(info) + ','
                                string_push += "None" + '\n'
                                file.write(string_push)
                        count += 1
                        index += 1
                        driver.back()
                        time.sleep(1)
                        products = driver.find_elements_by_xpath('//a[@class="product-item"]')
                driver.get(cat_href)
                driver.execute_script('''
            document.querySelectorAll('a[data-view-id="search_sort_item"]')[1].click()
        ''')
                time.sleep(1)
                count_sub_cate += 1
                sub_categories = driver.find_elements_by_xpath('//a[@class="item item--category "]')
        else:
            index = 0
            filename = unidecode.unidecode(cat_text)
            arr_words = filename.split(' ')
            filename_normal_form = ""
            for word in arr_words:
                filename_normal_form += word
            filename_normal_form = ".\data\electric_device\\" + filename_normal_form + ".csv"
            file = open(filename_normal_form,"a",encoding='utf-8')
            check_button_next = _check_button_next()
            if check_button_next == 1:
                while check_button_next == 1:
                    count = 0
                    products = driver.find_elements_by_xpath('//a[@class="product-item"]')
                    print(len(products))
                    while count < len(products) and products[count] is not None:
                        number_of_comment_count = 0
                        infos = get_info(cat_text,count)
                        #time.sleep(1)
                        check = check_next_button_comments()
                        element_product = []
                        if(check == 1):
                            while check == 1 and number_of_comment_count <= 500:
                                results = get_comments()
                                number_of_comment_count += len(results)
                                time.sleep(0.5)
                                check = check_next_button_comments()
                                for result in results:
                                    string_without_newline = clean_string(result)
                                    string_push = ""
                                    string_push += str(index) + ','
                                    for info in infos:
                                        string_push += str(info) + ','
                                    string_push += string_without_newline + '\n'
                                    file.write(string_push)
                                if number_of_comment_count == 0:
                                    string_push = ""
                                    string_push += str(index) + ','
                                    for info in infos:
                                        string_push += str(info) + ','
                                    string_push += "None" + '\n'
                                    file.write(string_push)
                                if check == 1:
                                    driver.execute_script(''' 
                                            document.querySelector('a[class="btn next"]').click();
                                    ''')
                        else:
                            results = get_comments()
                            number_of_comment_count += len(results)
                                #time.sleep(1)
                            for result in results:
                                string_without_newline = clean_string(result)
                                string_push = ""
                                string_push += str(index) + ','
                                for info in infos:
                                    string_push += str(info) + ','
                                string_push += string_without_newline + '\n'
                                file.write(string_push)
                            if number_of_comment_count == 0:
                                    string_push = ""
                                    string_push += str(index) + ','
                                    for info in infos:
                                        string_push += str(info) + ','
                                    string_push += "None" + '\n'
                                    file.write(string_push)
                        count += 1
                        index += 1
                        driver.back()
                        time.sleep(1)
                        products = driver.find_elements_by_xpath('//a[@class="product-item"]')
                    check_button_next = click_next_button()
                    time.sleep(1)
            else:
                count = 0
                products = driver.find_elements_by_xpath('//a[@class="product-item"]')
                print(len(products))
                while count < len(products) and products[count] is not None:
                    number_of_comment_count = 0
                    infos = get_info(cat_text,count)
                    #time.sleep(1)
                    check = check_next_button_comments()
                    element_product = []
                    if(check == 1):
                        while check == 1 and number_of_comment_count <= 500:
                            results = get_comments()
                            number_of_comment_count += len(results)
                            time.sleep(0.5)
                            check = check_next_button_comments()
                            for result in results:
                                string_without_newline = clean_string(result)
                                string_push = ""
                                string_push += str(index) + ','
                                for info in infos:
                                    string_push += str(info) + ','
                                string_push += string_without_newline + '\n'
                                file.write(string_push)
                            if number_of_comment_count == 0:
                                string_push = ""
                                string_push += str(index) + ','
                                for info in infos:
                                    string_push += str(info) + ','
                                string_push += "None" + '\n'
                                file.write(string_push)
                            if check == 1:
                                driver.execute_script(''' 
                                            document.querySelector('a[class="btn next"]').click();
                                    ''')
                    else:
                        results = get_comments()
                        number_of_comment_count += len(results)
                        for result in results:
                            string_without_newline = clean_string(result)
                            string_push = ""
                            string_push += str(index) + ','
                            for info in infos:
                                string_push += str(info) + ','
                            string_push += string_without_newline + '\n'
                            file.write(string_push)
                        if number_of_comment_count == 0:
                                string_push = ""
                                string_push += str(index) + ','
                                for info in infos:
                                    string_push += str(info) + ','
                                string_push += "None" + '\n'
                                file.write(string_push)
                    count += 1
                    index += 1
                    driver.back()
                    time.sleep(1)
                    products = driver.find_elements_by_xpath('//a[@class="product-item"]')
        count_cate += 1
        driver.get(url)
        
        categories = driver.find_elements_by_xpath('//a[@class="item item--category "]')
        time.sleep(1)
