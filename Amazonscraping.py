# coding:utf-8
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
import chromedriver_binary
import csv

def click_button(driver, xpath_button):
    button = driver.find_element_by_xpath(xpath_button)
    button.click()
    sleep(1)

def input_text(driver, input_xpath, input_text):
    input_element = driver.find_element_by_xpath(input_xpath)
    input_element.send_keys(input_text)
    sleep(1)

def save_csv(data, file_path):
    with open(file_path, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(data)

def get_product_title(product_title_xpath):
    try:
        product_title = driver.find_element_by_xpath(product_title_xpath).text
        sleep(1)
    except:
        product_title = ''
    return product_title

def get_review_value(review_value_xpath):
    try:
        review_value = driver.find_element_by_xpath(review_value_xpath).get_attribute("textContent").replace('5つ星のうち', '')
        sleep(1)
    except:
        review_value = ''
    return review_value

def get_review_number(review_number_xpath):
    try:
        review_number = driver.find_element_by_xpath(review_number_xpath).get_attribute("textContent").replace('個の評価', '').replace(',', '')
        sleep(1)
    except:
        review_number = ''
    return review_number

def get_price(price_xpath):
    try:
        price = driver.find_element_by_xpath(price_xpath).get_attribute("textContent").replace('￥', '').repalce(',', '')
        sleep(1)
    except:
        try:
            price = driver.find_element_by_xpath(price_timesale_xpath).get_attribute("textContent").replace('￥', '')
        except:
            price = ""
    return price

# xpath一覧
products_link_xpath = "//h2/a"
product_title_xpath = "//span[contains(@id, 'productTitle')]"
review_value_xpath = "//div[contains(@id, 'centerCol')]//span[contains(@class, 'a-icon-alt')]"
review_number_xpath = "//div[contains(@id, 'centerCol')]//span[contains(@id, 'acrCustomerReviewText')]"
price_xpath = "//div[contains(@id, 'centerCol')]//td[contains(text(), '価格')]/following-sibling::td/span[contains(@data-a-color,'price')]/span"
price_timesale_xpath = "//div[contains(@id, 'centerCol')]//td[contains(text(), '特選タイムセール')]/following-sibling::td/span[contains(@data-a-color,'price')]/span"


# 各種変数の定義
keyword = ""
page_numbers = ["1"]
product_detail = []

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)

for page_number in page_numbers:
    driver.get(f"https://www.amazon.co.jp/s?k={keyword}&page={page_number}")
    sleep(1)

    # 商品リンク一覧取得
    products = driver.find_elements_by_xpath(products_link_xpath)
    links = [product.get_attribute('href') for product in products]
    sleep(1)

    # 商品個別ページを表示
    for link in links:
        driver.get(link)
        sleep(1)

        product_title = get_product_title(product_title_xpath)
        price = get_price(price_xpath)
        review_value = get_review_value(review_value_xpath)
        review_number = get_review_number(review_number_xpath)

        product_detail.append([keyword, product_title, price, review_value, review_number])

# データの保存
save_csv(product_detail, 'amazon.csv')

# ブラウザを終了
driver.close()