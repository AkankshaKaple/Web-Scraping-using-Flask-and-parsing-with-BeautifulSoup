from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

input_name = "Niyo Solutions"
company_name = input_name + ' LinkedIn'
chromedriver = '/usr/bin/chromedriver'
browser = webdriver.Chrome(chromedriver)
browser.get('https://cse.google.com/cse?cx=015803321327240438025:r4xrjijfo_e')

c_name = browser.find_element_by_id('gsc-i-id1')
c_name.send_keys(company_name)
browser.find_element_by_class_name('gsc-search-button').click()
time.sleep(5)

data = browser.find_elements_by_tag_name('b')

time.sleep(3)

for i in data:
    if input_name in i.text:
        print(input_name, i.text)
        data_list = i.text
        i.click()
        data_list = i.text
        break
    else:
        pass

browser.switch_to_window(browser.window_handles[1])

browser.find_element_by_class_name('show-more-less-state__icon').click()

columns = ['Size', 'Headquarters', 'Website']
dict = {}

list_of_items = browser.find_element_by_class_name('about__primary-content')

for i in range(len(list_of_items.text.split('\n'))):
    data = list_of_items.text.split('\n')
    if data[i] in columns:
        dict[data[i]] = data[i+1]

print(dict)
