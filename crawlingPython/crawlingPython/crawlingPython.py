from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import html
import pymysql
import threading
 
TARGET_URL_BEFORE_PAGE_NUM = "http://news.donga.com/search?p="
TARGET_URL_BEFORE_KEWORD = '&query='
TARGET_URL_REST = '&check_news=2&more=1&sorting=1&search_date=4&v1=&v2=&range=1'


def deleteStr(str):
    result_str=str.replace('‘','')
    result_str=str.replace('’','')
    result_str=str.replace('“','')
    result_str=str.replace('”','')

    return result_str
 
# 기사 검색 페이지에서 기사 제목에 링크된 기사 본문 주소 받아오기
def get_link_from_news_title(page_num, URL,company):
    conn = pymysql.connect(host='db.cgxewdly4d7d.ap-northeast-2.rds.amazonaws.com',port=3306 ,user = 'hjgw',password='guswjdrldnd',database = 'news',charset='utf8' )
    curs = conn.cursor()
    sql_truncate="truncate table "+company
    curs.execute(sql_truncate)
    list_headline=[]
    list_contentUrl=[]
    list_time=[]
    list_date=[]
    list_img=[]
    list_content=[]
    
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

            

            # 내용 url 가져오기
            content_url = str(title_link[title_link.find('href="')+6:title_link.find('"',title_link.find('href="')+6)])
            
            

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
                
                
                check =2
            for s in date_time:
                if check is 1:

                    check =3
                elif check is 2:
                    break
                else:
                    if s.find('<span class') is not -1:
                        continue
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
                    
                        break
            list_headline.append(read_headline1)
            list_contentUrl.append(content_url)
            list_time.append(time)
            list_date.append(date)

        # 이미지 url 가져오기
        for title in soup.find_all('div', 'searchList'):
            if title.find('div','p') is not -1:
                img_url_tag = str(title.select('img'))
                img_url = str(img_url_tag[img_url_tag.find('src="')+5:img_url_tag.find('"',img_url_tag.find('src="')+5)])
                list_img.append(img_url)
            else:
                list_img.append("")
        
          
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
            list_content.append(contents1)
    #print(len(list_headline),len(list_content),len(list_contentUrl),len(list_date),len(list_time),len(list_img))
    for i in range(0,len(list_headline)): 
        company = str(company)
        date = str(date)
        time = str(time)
        sql ="insert into "+company+" (Headline,Content,ContentUrl,ImgUrl,NewsTime,NewsDate) values (%s, %s, %s, %s, %s, %s)"
        curs.execute( sql ,( deleteStr(list_headline[i]) ,deleteStr(list_content[i]) , list_contentUrl[i] , list_img[i] , list_time[i] , list_date[i]))
        #print(list_time[i] , list_date[i])
        #print(deleteStr(list_headline[i]) ,deleteStr(list_content[i]) , list_contentUrl[i] , list_img[i] ,list_time[i] , list_date[i])
        #print("-------------------------------------")
        conn.commit()   
    conn.close() 
 
# 기사 본문 내용 긁어오기 (위 함수 내부에서 기사 본문 주소 받아 사용되는 함수)
# 사용 x
def get_text(URL):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'html.parser', from_encoding='utf-8')
    content_of_article = soup.select('div.article_txt')
    for item in content_of_article:
        string_item = str(item.find_all(text=True))

def function():
    keyword = ['삼성','LG','현대','SK','네이버','카카오']
    for s in keyword:
        page_num =3
        target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEWORD \
                     + quote(s) + TARGET_URL_REST
        get_link_from_news_title(page_num, target_URL,s)
    threading.Timer(3600,function).start()


# 메인함수
def main():  
   function() 
   
   
     
   


if __name__ == '__main__':
    main()
