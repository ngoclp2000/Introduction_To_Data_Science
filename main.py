from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import re
import numpy as np

PATH = "E:\Selenium\chromedriver.exe"

driver = webdriver.Chrome(PATH)

urls = [
    'https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner',

]

for url in urls:
    index = 0
    rows = []
    rows.append(["index","name_product","price","number_of_comment","comment"])
    driver.get(url)
    time.sleep(1)
    check_button_next = driver.execute_script('''
    let ele =  document.querySelector('i[style="transform:rotate(180deg)"]');
            if (ele != null){
                return 1;
            }else return 0;
    ''')
    while check_button_next == 1:
        count = 0
        products = driver.find_elements_by_xpath('//a[@class="product-item"]')
        print(len(products))
        while count < len(products) and products[count] is not None:
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
            print(name)
            print(price)
            print(number_of_comment)
            time.sleep(1)
            check = driver.execute_script(''' 
                var element = document.querySelectorAll('.next')[1];
                if(typeof(element)  != 'undefined' && element != null){
                    return 1;
                }else return 0;

            ''')
            element_product = []
            while check:
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
                time.sleep(0.5)
                check = driver.execute_script(''' 
                var element = document.querySelectorAll('.next')[1];
                if(typeof(element)  != 'undefined' && element != null){
                    return 1;
                }else return 0;

                ''')
                if check == 1:
                    driver.execute_script(''' 
                        document.querySelectorAll('.next')[1].click();
                    ''')
                for result in results:
                    rows.append([index,name,price,number_of_comment,result])
            
            count += 1
            index += 1
            #print(rows)
            time.sleep(2)
            driver.back()
            products = driver.find_elements_by_xpath('//a[@class="product-item"]')
        check_button_next = driver.execute_script('''
        let x = document.querySelector('i[style="transform: rotate(180deg);"]');
        if (x != null && typeof(x) != undefined){
            return 1;
        }esle return 0;
        ''')
        if(check_button_next == 1): 
            driver.execute_script('''
                document.querySelector('i[style="transform: rotate(180deg).click();
            ''')
    a = np.asarray(rows)
    np.savetxt("data.csv",a,delimeter=",")
