from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
import os
import signal
from time import sleep
from selenium.webdriver.chrome.service import Service

s=Service(ChromeDriverManager().install())

error_flg = False


USERNAME = "aaaaaaaa"
PASSWORD = 'bbbbbbbb'
driver = webdriver.Chrome(webdriver.Chrome(ChromeDriverManager().install())) # よくわかんないけどこの形にしたら上手くいった笑

if error_flg is False:

    try:
        target_url = 'https://www.instagram.com'
        driver.get(target_url) 
    
        username_input = driver.find_element_by_xpath('//input[@aria-label="電話番号、ユーザーネーム、メールアドレス"]')
        username_input.send_keys(USERNAME)
        sleep(1)
 
        password_input = driver.find_element_by_xpath('//input[@aria-label="パスワード"]')
        password_input.send_keys(PASSWORD)
        sleep(1)
 
        username_input.submit()
        sleep(1)
        
    except Exception:
        print('ユーザー名、パスワード入力時にエラーが発生しました。')
        error_flg = True
    finally:
        os.kill(driver.service.process.pid,signal.SIGTERM) # chromedriverのプロセスだけ終了させてあげないと、プラウザも一緒に終了してしまう

