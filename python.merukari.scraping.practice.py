from selenium import webdriver
import time
import pandas
from webdriver_manager.chrome import ChromeDriverManager 
import os
import signal

#キーワード入力
search_word = input("検索キーワード＝")

# メルカリ
url =  'https://www.mercari.com/jp/search/?keyword=' + search_word

# chromedriverの設定とキーワード検索実行
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

os.kill(driver.service.process.pid,signal.SIGTERM)

item_name = driver.find_elements_by_class_name("heading page")

print(item_name)