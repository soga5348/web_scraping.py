#メルカリ収益自動取得プログラム

import pandas as pd
from selenium import webdriver
import time
import csv
import os

#Pandas.dfの準備
columns = ["商品ID","商品名", "価格", "送料負担","販売手数料", "送料","販売利益","販売日時"]

#chromeの起動
options = webdriver.chrome.options.Options()
profile_path = '/Users/sogasyunto/Library/Application Support/Google/Chrome/Default'
options.add_argument('--user-data-dir=' + profile_path)
browser = webdriver.Chrome("./chromedriver", options=options)
time.sleep(5)    #起動時に時間がかかるため、5秒スリープ

# 出品した商品ページから商品IDを取得する関数
def item_id_get(url):
    item_id = []
    try:
        while(True):
    
            browser.get(url)
            posts = browser.find_elements_by_css_selector(".js-mypage-item")
   
            for post in posts:
                # 商品IDの取得
                item_id.append(post.get_attribute("data-item-id"))
        
            next_url = browser.find_element_by_css_selector(
                    "li.pager-next.pager-cell a").get_attribute("href")
            if next_url != url:
                url = next_url
            else:
                break
    except:
        print("item_id_getは中断されました。")
        import traceback
        traceback.print_exc()
    
    return item_id


# 商品IDから販売情報を取得する関数
def info_get(item_id):
    browser.get("https://www.mercari.com/jp/transaction/order_status/" + item_id + "/")
    posts = browser.find_elements_by_css_selector(".transact-info-table-cell")
    raw_info = []
    for post in posts:
        raw_info.append(post.text)
        # df向けに整形
    
    name_price = raw_info[1].split("\n")
    info = pd.Series([item_id,name_price[0], name_price[1], raw_info[3], raw_info[5], 
                        raw_info[7], raw_info[9], raw_info[11]], columns)        
    return info

#main関数
def main():
    
    df = pd.DataFrame(columns=columns)
    
    #売却済みの全商品IDをリストで取得する
    url = "https://www.mercari.com/jp/mypage/listings/completed/"
    item_id_list  = item_id_get(url)

    #商品IDごとに販売情報を取得してdfに追加
    index = 0
    index_max = len(item_id_list)
    try:
        while(True):
            info = info_get(item_id_list[index])
            df = df.append(info,columns)
            index += 1
            if index >= index_max:
                break
            time.sleep(2)    #大量リクエストの防止で２秒止める
    except:
        print("info_getは中断されました。")
        import traceback
        traceback.print_exc()
     
    #csvを保存する
    filename = "メルカリ販売リスト" + ".csv"
    df.to_csv(filename, encoding="utf-8-sig")
    
    #chromeを閉じる
    browser.quit()
    
    return print("Finish!")
        

main()