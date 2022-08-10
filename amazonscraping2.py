from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import textwrap
import csv
 
#windows(chromedriver.exeのパスを設定)
chrome_path = r'C:\Users\デスクトップ\python\selenium_test\chromedriver'
 
#mac
#chrome_path = 'C:/Users/デスクトップ/python/selenium_test/chromedriver'
 
#　amazonのレビュー情報をseleniumで取得する_引数：amazonの商品URL
def get_amazon_page_info(url):
    text = ""                               #　初期化
    options = Options()                     #　オプションを用意
    options.add_argument('--incognito')     #　シークレットモードの設定を付与
    #　chromedriverのパスとパラメータを設定
    driver = webdriver.Chrome(executable_path=chrome_path,options=options)
    driver.get(url)                         #　chromeブラウザでurlを開く
    driver.implicitly_wait(10)              #　指定したドライバの要素が見つかるまでの待ち時間を設定
    text = driver.page_source               #　ページ情報を取得
    
    driver.quit()                           #　chromeブラウザを閉じる
    
    return text                             #　取得したページ情報を返す
 
# 全ページ分をリストにする
def get_all_reviews(url):
    review_list = []                        #　初期化
    i = 1                                   #　ループ番号の初期化
    while True:
        print(i,'page_search')              #　処理状況を表示
        i += 1                              #　ループ番号を更新
        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する
        amazon_bs = BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
        reviews = amazon_bs.select('.review-text')          #　ページ内の全レビューのテキストを取得
        
        for review in reviews:                              #　取得したレビュー数分だけ処理を繰り返す
            review_list.append(review)                      #　レビュー情報をreview_listに格納
             
        next_page = amazon_bs.select('li.a-last a')         # 「次へ」ボタンの遷移先取得
        
        # 次のページが存在する場合
        if next_page != []: 
            # 次のページのURLを生成   
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']    
            url = next_url  # 次のページのURLをセットする
            
            sleep(1)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
 
    return review_list
 
#インポート時は実行されないように記載
if __name__ == '__main__':
     
    #　Amzon商品ページ
    url = 'https://www.amazon.co.jp/%E3%83%89%E3%82%A6%E3%82%B7%E3%82%B7%E3%83%A3-%E3%82%BF%E3%83%B3%E3%83%96%E3%83%A9%E3%83%BC-%E7%8C%AB%E8%88%8C%E5%B0%82%E7%A7%91%E3%82%BF%E3%83%B3%E3%83%96%E3%83%A9%E3%83%BC-320ml-%E3%82%B0%E3%83%AA%E3%83%BC%E3%83%B3/dp/B08MW6YQY5/ref=pd_rhf_cr_s_bmx_5?pd_rd_w=1MuoR&pf_rd_p=b35c88ee-075c-481c-ab75-32553855cd5b&pf_rd_r=W5W6QVTMA9PPK89776SH&pd_rd_r=49445fb8-416e-4f67-a3cf-6b650ea6659c&pd_rd_wg=mRwDl&pd_rd_i=B08MW6YQY5&psc=1'
    
    # URLをレビューページのものに書き換える
    review_url = url.replace('dp', 'product-reviews')
    # レビュー情報の取得
    review_list = get_all_reviews(review_url)    
 
    #CSVにレビュー情報の書き出し
    #with open('data/sample.csv','w') as f:　#Windowsでエンコードエラーになる場合があるため下の行に変更
    with open('data/sample.csv','w',encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
 
        # 全データを表示
        for i in range(len(review_list)):
            csvlist=[]
            review_text = textwrap.fill(review_list[i].text, 500)
            #データ作成
            csvlist.append('No.{} : '.format(i+1))      #　便宜上「No.XX」の文字列を作成
            csvlist.append(review_text.strip())         #　レビューテキストの先頭・末尾の空白文字を除去
            # 出力    
            writer.writerow(csvlist)                    
        # ファイルクローズ
        f.close()
