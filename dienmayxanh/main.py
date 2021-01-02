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



PATH = "E:\Selenium\Introduction_To_Data_Science\chromedriver.exe"

driver = webdriver.Chrome(PATH)
urls = [
    'https://www.dienmayxanh.com/dien-thoai?g=dien-thoai-pho-thong&page=0#g:62879',
    'https://www.dienmayxanh.com/dien-thoai?g=iphone-ios&page=0#g:39238',
    'https://www.dienmayxanh.com/dien-thoai?g=android#g:39237'
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

def get_infor():
    name = driver.find_element_by_css_selector('h1').text()
    price = driver.find_element_by_css_selector('.displayp').text()
    number_of_comment = driver.find_element_by_class_name('.tltRt').text()
    re.findall('[0-9]+',number_of_comment)
    description = driver.execute_script('''
        let arr = [];
        document.querySelector('.viewparameterfull').click();
        
    ''')

for url in urls:
    driver.get(url)
    driver.execute_script('''
        
            x = document.querySelector('.loadmore');
            while ( x != null){
                x.click();
                x = document.querySelector('.loadmore');
            }
        
    ''')
    products = driver.find_elements_by_class_name('prdItemGetDelStt')
    for product in products:
        driver.get(product.get_attribute("href"))
        infos = get_infor()
    print(len(products))
    time.sleep(1.5)
    

