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
PATH = "E:\Selenium\Introduction_To_Data_Science\chromedriver.exe"

driver = webdriver.Chrome(PATH)
file = open(".\data\electric_device.csv","a",encoding='utf-8')
urls = [
    'https://tiki.vn/tivi-thiet-bi-nghe-nhin/c4221?src=c.4221.hamburger_menu_fly_out_banner',

]

for url in urls:
    page_count = 1
    index = 0
    #rows = []
    #rows.append(["index","name_product","price","number_of_comment","comment"])
    #file.write("index,name_product,price,number_of_comment,comment\n")
    driver.get(url)
    time.sleep(1)
    check_button_next = driver.execute_script('''
    let t1 = document.querySelector('i[style="transform: rotate(180deg);"]');
    let t2 = document.querySelector('i[style="transform:rotate(180deg)"]');
    let t3 = document.querySelector('i[style="transform:rotate(180deg);"]');
    let t4 = document.querySelector('i[style="transform: rotate(180deg)"]');
    if (t1 != null || t2 != null || t3 != null || t4 != null){
                return 1;
    }else return 0;
    ''')
    while check_button_next == 1:
        if index < 146:
            index += 1
            continue
        elif index == 146:
            index+=1
            for i in range(3):
                driver.execute_script('''
                let t1 = document.querySelector('i[style="transform: rotate(180deg);"]');
                    let t2 = document.querySelector('i[style="transform:rotate(180deg)"]');
                    let t3 = document.querySelector('i[style="transform:rotate(180deg);"]');
                    let t4 = document.querySelector('i[style="transform: rotate(180deg)"]');
                    if (t1 != null){
                        t1.click();
                    }else if(t2 != null){
                        t2.click();
                    }else if (t3 != null){
                        t3.click();
                    }else{
                        t4.click();
                    }
                ''')
                time.sleep(1)
        count = 0
        products = driver.find_elements_by_xpath('//a[@class="product-item"]')
        print(len(products))
        while count < len(products) and products[count] is not None:
            number_of_comment_count = 0
            name = driver.find_elements_by_xpath(
                '//div[@class="name"]/span')[count].text
            price = driver.find_elements_by_xpath(
                '//div[@class="price-discount__price"]')[count].text
            
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
            print(name)
            print(price)
            print(number_of_comment)
            time.sleep(1)
            check = driver.execute_script(''' 
                let element = document.querySelector('a[class="btn next"]');
                if( element != null){
                    return 1;
                }else return 0;

            ''')
            element_product = []
            if(check == 1):
                while check == 1 and number_of_comment_count <= 500:
                    results = driver.execute_script('''
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
                    number_of_comment_count += len(results)
                    time.sleep(0.5)
                    check = driver.execute_script(''' 
                        let element = document.querySelector('a[class="btn next"]');
                        if( element != null){
                            return 1;
                        }else return 0;

                    ''')
                    if check == 1:
                        driver.execute_script(''' 
                            document.querySelector('a[class="btn next"]').click();
                        ''')
                    for result in results:
                        result = result.replace('\n',' ')
                        result = result.replace(',',';')
                        result = result.replace(':','')
                        result = result.replace('-','')
                        string_without_newline = ""
                        for c in result:
                            if c.isalpha() or c.isdigit() or c == ' ':
                                string_without_newline += c
                        string_push = str(index) + "," + name + "," + str(price) + "," + str(number_of_comment) + "," + string_without_newline + "\n"
                        #print(string_push.encode('utf-8'))
                        file.write(string_push)
                        #rows.append([index,name,price,number_of_comment,result])
            else:
                results = driver.execute_script('''
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
                number_of_comment_count += len(results)
                #time.sleep(1)
                for result in results:
                    result = result.replace('\n',' ')
                    result = result.replace(',',';')
                    result = result.replace(':','')
                    result = result.replace('-','')
                    string_push = str(index) + "," + name + "," + str(price) + "," + str(number_of_comment) + "," + result + "\n"
                        #print(string_push.encode('utf-8'))
                    file.write(string_push)
            count += 1
            index += 1
            #print(rows)
            driver.back()
            time.sleep(1)
            products = driver.find_elements_by_xpath('//a[@class="product-item"]')
        driver.execute_script('''
               let t1 = document.querySelector('i[style="transform: rotate(180deg);"]');
                let t2 = document.querySelector('i[style="transform:rotate(180deg)"]');
                let t3 = document.querySelector('i[style="transform:rotate(180deg);"]');
                let t4 = document.querySelector('i[style="transform: rotate(180deg)"]');
                if (t1 != null){
                    t1.click();
                }else if(t2 != null){
                    t2.click();
                }else if (t3 != null){
                    t3.click();
                }else{
                    t4.click();
                }
        ''')
    
    # for i in range(len(rows)):
    #     for j in range(len(rows[i])):
    #         file.write(rows[i][j])
    #         if j != len(rows[i])- 1 : file.write(",")
    #     file.write("\n")
