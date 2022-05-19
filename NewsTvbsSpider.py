import requests
import re
from bs4 import BeautifulSoup

url = 'https://news.tvbs.com.tw/world'
web = requests.get(url)
soup = BeautifulSoup(web.text, 'html.parser')
news_now2_div_tag = soup.find('div',class_='news_now2')
soup2 = BeautifulSoup(str(news_now2_div_tag), 'html.parser')
a_tags = soup2.findAll('a')

with open('A.txt', 'w') as f:
    for i in range(3):
        print('https://news.tvbs.com.tw' + a_tags[i].get('href'))
        web2 = requests.get('https://news.tvbs.com.tw' + a_tags[i].get('href'))
        soup3 = BeautifulSoup(web2.text, 'html.parser')
        # date
        author_div_tag = soup3.find('div',class_='author')
        date = re.search('發佈時間：(.+?) ', str(author_div_tag))
        data_dict = dict()
        data_dict['date'] = date.group(1).strip()
        # article
        article_div_tag = soup3.find('div',class_='article_content')
        article = ''
        for paragraph in article_div_tag.text.split():
            article += paragraph
        data_dict['article'] = article
        f.write(str(data_dict) + '\n')
        
        



