# 股票数据定向爬虫
import re
import requests
from bs4 import BeautifulSoup
import traceback


# 函数功能：原始数据爬取
def getHtmlText(url):
    try:
        r = requests.get(url)
        # r.encoding = r.apparent_encoding
        r.encoding = 'utf-8'
        r.raise_for_status()
        # print(r.text[-500:])
        return r.text
    except:
        traceback.print_exc()


# 函数功能：获取股票列表
def getStockList(lst, stockListURL):
    ra = [11, 12, 13, 14, 15, 16, 17]
    # ra = [11]
    count = 1
    for i in ra:
        stock_list_html = getHtmlText(stockListURL + str(i))
        soup = BeautifulSoup(stock_list_html, "html.parser")
        a = soup.find_all('a')
        for i in a:
            try:
                href = i.attrs["href"]
                stock_a = re.search(r'\d{6}.html$', href)
                if stock_a:
                    count += 1
                    lst.append(stock_a.group(0))
            except:
                traceback.print_exc()
    return count


# 函数功能：进入每个股票的链接，爬取对应股票的相关信息
def getStockInfo(lis, stockInfoURL, fpath, count):
    ready_count = 0
    f = open(fpath, 'a', encoding='utf-8')
    for j in lis[:100]:
        stock_info_html = getHtmlText(stockInfoURL + str(j))
        # print(stock_info_html)
        try:
            if stock_info_html == '':
                continue
            # 每个股票存为字典，数据处理较麻烦，有些数据有“杂音”，需单独给出if判断，或在正则中约束
            infoDict = {}
            soup = BeautifulSoup(stock_info_html, "html.parser")
            stockInfo = soup.find('div', attrs={'id': 'act_quote'})
            name = stockInfo.find('div', attrs={'class': 'Lfont'}).string
            # print(name)
            infoDict.update({'股票名称': name})
            stockDetialInfo = stockInfo.find('table', attrs={'id': 'quotetab_stock'})
            td = stockDetialInfo.find_all("td")
            # print(td)
            for item in td:
                # print(item.get_text())
                text = item.get_text()
                if (text == "业绩预告"):
                    print("hear")
                    key = "业绩预告"
                    real_val = "业绩预告"
                else:
                    text_split = re.split(':|：', text)  # 网站程序员分号用了中文和英文两种……
                    key = text_split[0]
                    val = text_split[1]
                    real_val = re.search(r'(-?\d+.?\d*[%|手|万|元]?)|(--)|(正无穷大)', val).group(0)

                infoDict[key] = real_val
            f.write(str(infoDict) + '\n')  # 每个股票字典数据转为字符串写入文件
            ready_count += 1
            print('\r当前第{0:}个,共{1:}个'.format(ready_count, count))  # 打印进度

        except:
            print('\r当前第{0:}个,共{1:}个'.format(ready_count, count))
            traceback.print_exc()
    f.close()


def main():
    lst = []
    stock_list_url = "http://quote.cfi.cn/stockList.aspx?t="  # 股票列表，翻页接口
    stock_info_url = "http://quote.cfi.cn/"  # 每个股票的链接都是http://quote.cfi.cn/000000.html的形式。000000代表六位的股票代码
    output_path = "C:\\Users\\管筠箫\\PycharmProjects\\pythonProject\\StockInfo.txt"
    stock_count = getStockList(lst, stock_list_url)
    # stock_count = 100
    getStockInfo(lst, stock_info_url, output_path, stock_count)


main()
