from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
 
TARGET_URL_BEFORE_PAGE_NUM = "http://news.donga.com/search?p="
TARGET_URL_BEFORE_KEWORD = '&query='
TARGET_URL_REST = '&check_news=2&more=1&sorting=1&search_date=4&v1=&v2=&range=1'
 
 
# 기사 검색 페이지에서 기사 제목에 링크된 기사 본문 주소 받아오기
def get_link_from_news_title(page_num, URL):
    for i in range(page_num):
        current_page_num = 1 + i*15
        position = URL.index('=')
        URL_with_page_num = URL[: position+1] + str(current_page_num) + URL[position+1 :]
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'html.parser',from_encoding='utf-8')
        for title in soup.find_all('p', 'tit'):
            title_link = str(title.select('a'))
            print (title_link[str(title_link).find('>')+1:str(title_link).find('<',str(title_link).find('>')+1)])
            title_length = title_link.find('<',str(title_link).find('>')+1)
            if title_link.find('<span class') is not -1 :
                 print (title_link[str(title_link).find('light">')+7:str(title_link).find('</span>')])
                 print (title_link[str(title_link).find('</span>')+7:str(title_link).find('</a>')])

            
            
 
# 기사 본문 내용 긁어오기 (위 함수 내부에서 기사 본문 주소 받아 사용되는 함수)
def get_text(URL):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'html.parser', from_encoding='utf-8')
    content_of_article = soup.select('div.article_txt')
    for item in content_of_article:
        string_item = str(item.find_all(text=True))
 
 
# 메인함수
def main():   
    keyword = '사드'
    page_num =3
    target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEWORD \
                 + quote(keyword) + TARGET_URL_REST
    get_link_from_news_title(page_num, target_URL)

 
if __name__ == '__main__':
    main()
