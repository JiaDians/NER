import requests
import re
from bs4 import BeautifulSoup
import sys

url1 = 'https://news.tvbs.com.tw/world' # 全球
url2 = 'https://news.tvbs.com.tw/local' # 社會


def GetData(date):
    web = requests.get(url2)    # set url
    soup = BeautifulSoup(web.text, 'html.parser')
    news_now2_div_tag = soup.find('div',class_='news_now2')
    soup2 = BeautifulSoup(str(news_now2_div_tag), 'html.parser')
    a_tags = soup2.findAll('a')
    
    with open('A.txt', 'w', encoding='UTF-8') as f:
        for i in range(8):
            print('https://news.tvbs.com.tw' + a_tags[i].get('href'))
            web2 = requests.get('https://news.tvbs.com.tw' + a_tags[i].get('href'))
            soup3 = BeautifulSoup(web2.text, 'html.parser')
            # date
            author_div_tag = soup3.find('div',class_='author')
            date = re.search('發佈時間：(.+?) ', str(author_div_tag))
            data1_dict = dict()
            data1_dict['date'] = date.group(1).strip()
            # print(data1_dict['date'], date.group(1))
            if date.group(1) != data1_dict['date']:
                print('this article is wrong date')
                continue
            # article
            article_div_tag = soup3.find('div',class_='article_content')
            soup4 = BeautifulSoup(str(article_div_tag), 'html.parser')
            
            # 移除 宣傳標題
            del_tags = soup4.find_all("div", {"class":"guangxuan"})
            for del_tag in del_tags:
                del_tag.extract()
            del_tags = soup4.find_all("span", {"class":"endtext"})
            for del_tag in del_tags:
                del_tag.extract()
            del_tags = soup4.find_all("strong")
            for del_tag in del_tags:
                del_tag.extract()
            article = '' 
            article_div_tag = soup4.find('div',class_='article_content')
            for paragraph in article_div_tag.text.split():
                article += paragraph.replace('\'','\"')
            
            data1_dict['article'] = article
            f.write(str(data1_dict) + '\n', )
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('no argument')
        sys.exit()
    print('hello')
    print(sys.argv[0])
    print(sys.argv[1])
    DateRegex = re.compile(r'\d\d\d\d/\d\d/\d\d')
    result = DateRegex.findall(sys.argv[1])
    if len(result) == 1:
        GetData(result[0])
    else:
        print('wrong parameter format')
        



