from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import html
 
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

            #기사 헤드라인 
            title_link = str(title.select('a'))
            read_headline1= str(title_link[str(title_link).find('>')+1:str(title_link).find('<',str(title_link).find('>')+1)])
            index = title_link.find('<a')
            while 1:
                if title_link.find('<span class',index) is not -1:
                     read_headline1 += str(title_link[str(title_link).find('light">',index)+7:str(title_link).find('</span>',index)])
                     index = title_link.find('</span>',index)
                     if title_link.find('<span',index) is not -1:
                         read_headline1 += str(title_link[title_link.find('</span>',index)+7:str(title_link).find('<span',index)])
                         index = title_link.find('<span class',index)
                         continue
                     else:
                         read_headline1 += str(title_link[str(title_link).find('</span>',index)+7:str(title_link).find('</a>',index)])
                         break
                else:
                    break
            print (read_headline1)
            

            # 기사 시간, 날짜 
            title_time = str(title.select('span'))
            if title_time.find('<span class') is not -1:
                date_time = title_time.split('</span>')
                check=1;
            else:
                date_time = str(title_time[title_time.find('<span>')+6:title_time.find('</span>')])
                split_date_time = date_time.split(' ')
                loop_check=0;
                for loop in split_date_time:
                    if loop_check is 0:
                        date = loop
                        loop_check =1
                    else:
                        time = loop
                print (date)  # 날짜
                print (time)  # 시간
                check =2
            for s in date_time:
                if check is 1:
                    check =3
                elif check is 2:
                    break
                else:
                    n_date_time = s
                    date_time_str = str(n_date_time[str(n_date_time).find('<span>')+6:])
                    split_date_time_n = date_time_str.split(' ')
                    loop_check=0;
                    for loop in split_date_time_n:
                        if loop_check is 0:
                            date = loop
                            loop_check =1
                        else:
                            time = loop
                    print (date)  # 날짜
                    print (time)  # 시간
                    break

          
        # 기사 요약 내용 가져오기   

        for title_contents in soup.find_all('p', 'txt'):
            contents_txt = str(title_contents.select('a'))
            contents1 = str(contents_txt[str(contents_txt).find('blank">')+7:str(contents_txt).find('<',str(contents_txt).find('blank">'))])
            index = contents_txt.find('<a')
            while 1:
                if contents_txt.find('<span class',index) is not -1:
                     contents1 += str(contents_txt[str(contents_txt).find('light">',index)+7:str(contents_txt).find('</span>',index)])
                     index = contents_txt.find('</span>',index)
                     if contents_txt.find('<span',index) is not -1:
                         contents1 += str(contents_txt[contents_txt.find('</span>',index)+7:str(contents_txt).find('<span',index)])
                         index = contents_txt.find('<span class',index)
                         continue
                     else:
                         contents1 += str(contents_txt[str(contents_txt).find('</span>',index)+7:str(contents_txt).find('</a>',index)])
                         break
                else:
                    break

            print (contents1)
            


 
# 기사 본문 내용 긁어오기 (위 함수 내부에서 기사 본문 주소 받아 사용되는 함수)
def get_text(URL):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'html.parser', from_encoding='utf-8')
    content_of_article = soup.select('div.article_txt')
    for item in content_of_article:
        string_item = str(item.find_all(text=True))
 
 
# 메인함수
def main():   
    keyword = '삼성'
    page_num =3
    target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEWORD \
                 + quote(keyword) + TARGET_URL_REST
    get_link_from_news_title(page_num, target_URL)

 
if __name__ == '__main__':
    main()
