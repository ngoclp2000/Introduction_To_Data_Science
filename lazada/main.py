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
file = open("data.csv","a",encoding='utf-8')
urls = [
    'https://www.lazada.vn/dien-thoai-may-tinh-bang/?spm=a2o4n.searchlistcategory.breadcrumb.2.50f261c08nJzeh',

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
    let x = document.querySelector('li[title="Next Page"]');
    if (x != null){
                return 1;
    }else return 0;
    ''')
    while check_button_next == 1:
        count = 0
        products = driver.find_elements_by_xpath('//a[@class="c2prKC"]')
        print(len(products))
        while count < len(products) and products[count] is not None:
            number_of_comment_count = 0
            name = driver.find_elements_by_xpath(
                '//div[@class="c16H9d"]')[count].text
            price = driver.find_elements_by_xpath(
                '//div[@class="c13VH6"]')[count].text
            
            driver.get(products[count].get_attribute("href"))
            time.sleep(1)

            number_of_comment = driver.execute_script('''
            let ele =  document.querySelector('a[class="pdp-link pdp-link_size_s pdp-link_theme_blue pdp-review-summary__link"]');
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
                var element = document.querySelector('i[class="next-icon next-icon-arrow-right next-icon-medium next-icon-last"]');
                if(typeof(element)  != 'undefined' && element != null){
                    return 1;
                }else return 0;

            ''')
            element_product = []
            if(check == 1):
                while check == 1 and number_of_comment_count <= 500:
                    results = driver.execute_script('''
                    cells = document.querySelectorAll('.content');
                    let count = 0;
                    cms = [];
                    [].forEach.call(cells, function (el) {
                        if(count == 0){
                            count++;
                            continue;
                        }
                        if(el.textContent != '' ){
                            cms.push(el.textContent);
                        }
                        count += 1;
                    });
                    return cms
                    ''')
                    number_of_comment_count += len(results)
                    time.sleep(0.5)
                    check = driver.execute_script(''' 
                    var element = document.querySelector('i[class="next-icon next-icon-arrow-right next-icon-medium next-icon-last"]');
                    if(typeof(element)  != 'undefined' && element != null){
                        return 1;
                    }else return 0;

                    ''')
                    if check == 1:
                        driver.execute_script(''' 
                            document.querySelector('i[class="next-icon next-icon-arrow-right next-icon-medium next-icon-last"]').click();
                        ''')
                    for result in results:
                        result = result.replace('\n',' ')
                        string_push = str(index) + "," + name + "," + str(price) + "," + str(number_of_comment) + "," + result + "\n"
                        #print(string_push.encode('utf-8'))
                        file.write(string_push)
                        #rows.append([index,name,price,number_of_comment,result])
            else:
                results = driver.execute_script('''
                    cells = document.querySelectorAll('.content');
                    let count = 0;
                    cms = [];
                    [].forEach.call(cells, function (el) {
                        if(count == 0){
                        count += 1;
                        continue;
                        }
                        if(el.textContent != '' ){
                            cms.push(el.textContent);
                        }
                        count += 1;
                    });
                    return cms
                    ''')
                number_of_comment_count += len(results)
                #time.sleep(1)
                for result in results:
                    result = result.replace('\n',' ')
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
               let x = document.querySelector('li[title="Next Page"]');
               if(x != null){
                x.click();
               }
            ''')
        page_count+=1
    
    # for i in range(len(rows)):
    #     for j in range(len(rows[i])):
    #         file.write(rows[i][j])
    #         if j != len(rows[i])- 1 : file.write(",")
    #     file.write("\n")
