# 『河合その子サイン』とかで検索すると検索結果が少なくてデバッグモードが行いやすい

from selenium import webdriver
import time
import pandas                                                      # pandasモジュールは、取得したデータをCSVファイルに出力するために利用します
from webdriver_manager.chrome import ChromeDriverManager

#キーワード入力
search_word = input("検索キーワード＝")

# メルカリ
url =  'https://www.mercari.com/jp/search/?keyword=' + search_word

# chromedriverの設定とキーワード検索実行
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1200,1000)
driver.get(url)

# ページカウントとアイテムカウント用変数
page = 1
item_num = 0
item_urls = []

while True:
    print("Getting the page {} ...".format(page))                                       # printする際の表示方法、formatメソッドによって{}にpageを表示させている。
    time.sleep(1)
    items = driver.find_elements_by_class_name("ItemGrid__ItemGridCell-sc-14pfel3-1")   # ItemGrid__ItemGridCell-sc-14pfel3-1は、ul列のli要素になっており検索結果で表示される個別の画像に対して、検証モードを行うことでclass名ということで表示される。
    for item in items:
        item_num += 1
        item_url = item.find_element_by_css_selector("a").get_attribute("href")       # aタグ内にあるhref属性の指定ということであるがURLの指定等、頻繁に用いられるものらしい。
        print("item{0} url:{1}".format(item_num, item_url))                           # デバッグで出力させてみるとわかるんだけど、formatメソッドを用いていてそれぞれ{}{}内に埋め込まれているものを出力している。
        item_urls.append(item_url)
    page += 1                                                                         # 31行目から33行目に行く際そのまま↓移動する

    try:
        next_page = driver.find_element_by_class_name("icon inherit") # 多分だけどこの行で次ページ（が存在する場合）の要素取得を行っている。
        driver.get(next_page)
        print("next url:{}".format(next_page))
        print("Moving to the next page...")
    except:
        print("Last page!")
        break

# アイテムカウントリセットとデータフレームセット
item_num = 0
columns = ["item_name", "cat1", "cat2", "cat3", "brand_name", "product_state", "price", "url"]
df = pandas.DataFrame(columns=columns)

try: # エラーで途中終了時をtry～exceptで対応
    # 取得した全URLを回す
    for product_url in item_urls:
        item_num += 1
        print("Moving to the item {}...".format(item_num))
        time.sleep(1)
        driver.get(product_url)

        time.sleep(2)
        item_name = driver.find_element_by_xpath("//mer-heading[@class='mer-spacing-b-2']").get_attribute("title-label") # mer-headingタグの、class名mer-spacing-b-2のtitle-labelの要素が抜き出されている。
        print("Getting the information of {}...".format(item_name))                                                      # xpathによって指定を行う場合、タグ名の前に//で指定するっぽい

        cat = driver.find_elements_by_xpath("//a[@data-location='item:item_detail_table:link:go_search']")               # 自分が欲している情報は何なのかを意識して検証モードを行うと答えが見えたりする笑
        cat1 = cat[0].accessible_name                                                                                    # この場合、カテゴリー名を欲しているのでカテゴリーのボタン上で検証モードを行うとできる（多分あってるのだと思う）
        cat2 = cat[1].accessible_name                                                                                    # ちょっと調べても微妙だったんだけど、どうやらこのaccessivle_nameというものを使うと簡単にweb上の情報にアクセスできるんだとさ
        cat3 = cat[2].accessible_name
        try: # 存在しない⇒a, divタグがない場合をtry～exceptで対応
            brand_name = driver.find_element_by_css_selector("table.item-detail-table tbody tr:nth-child(3) td a div").text # ちょっと要素の解析がわからなかったけど、ブランドタグが設定されてあるやつも上手く出力されないことからサイトの形式が変わったと思われる。
        except:                                                                                                             # ただtr:nth-child(3)ってのはcss_selectorで要素を抜き出す際にtrリストの4番目の要素を抜き出すことを意味してるっぽい。
            brand_name = ""

        product_state = driver.find_element_by_xpath("//span[@data-testid='商品の状態']").text
        price = driver.find_element_by_xpath("//mer-price").get_attribute("value")
        price = price.replace("¥", "").replace(" ","").replace(",", "")                                                 # replace関数？の使用

        print(cat1)
        print(cat2)
        print(cat3)
        print(brand_name)
        print(product_state)
        print(price)
        print(product_url)

        se = pandas.Series([item_name, cat1, cat2, cat3, brand_name, product_state, price, product_url], columns)      # pandas.Seriesによってリストのデータをシリーズ化している。
        df = df.append(se, ignore_index=True)                                                                          # indexとはcsvへの出力の際の表記方法？要復習
        print("Item {} added!".format(item_num))

except:
   print("Error occurred! Process cancelled but the added items will be exported to .csv")

#df.to_csv("{}.csv".format(search_word), index=False, encoding="utf_8")
df.to_csv("{}.csv".format(search_word), index=False, encoding="utf_8_sig")                                            # これを使うことでデータフレームに格納されているデータをCSVファイルへと書き出せる。
driver.quit()

print("Scraping is complete!")