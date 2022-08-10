from tkinter import BROWSE # ブラウズ機能のインポート
from selenium import webdriver # webdriver機能のインポート
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep # time機能のインポート
import os, signal


browser = webdriver.Chrome(ChromeDriverManager().install())

url = 'https://scraping-for-beginner.herokuapp.com/login_page'
browser.get(url)
sleep(3)

elem_username = browser.find_element_by_id("username")
elem_username.send_keys("imanishi")

elem_password = browser.find_element_by_id("password")
elem_password.send_keys("kohei")

elem_login_btn = browser.find_element_by_id("login-btn")
elem_login_btn.click()

# browser.quit()
os.kill(browser.service.process.pid, signal.SIGTERM)