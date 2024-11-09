import html.parser
from lxml.html import HTMLParser
import requests
from lxml import etree
import json
import pymongo
client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client["zhiwang"]
collection=db['newspider']
session=requests.session()
url='https://search.cnki.com.cn/api/search/listresult'
headers={
    "Cookie":'SID_search=017049; UM_distinctid=192fcc638d5109d-085daca5c9bcf6-26011951-1fa400-192fcc638d68c6; KEYWORD=%E5%8C%BA%E5%9D%97%E9%93%BE; CNZZDATA1257838124=1009648038-1730817702-%7C1730817754',
    'referer':'https://search.cnki.com.cn/Search/Result',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}
def get_message(filename):
    url='https://www.cnki.com.cn/Article/CJFDTOTAL-'+filename+'.htm'
    print(url)
    return url
def find_filename(theme=None,title=None,keywd=None,author=None,page=1):

    data={
        'searchType': 'MulityTermsSearch',
        'ArticleType': 0,
        'ReSearch': '',
        'ParamIsNullOrEmpty': 'false',
        'Islegal': 'false',
        'Content': '',
        'Theme': theme,
        'Title': title,
        'KeyWd': keywd,
        'Author': author,
        'SearchFund':'' ,
        'Originate':'' ,
        'Summary': '',
        'PublishTimeBegin': '',
        'PublishTimeEnd': '',
        'MapNumber':'' ,
        'Name': '',
        'Issn': '',
        'Cn': '',
        'Unit': '',
        'Public': '',
        'Boss':'' ,
        'FirstBoss':'' ,
        'Catalog':'' ,
        'Reference':'' ,
        'Speciality':'' ,
        'Type':'' ,
        'Subject':'' ,
        'SpecialityCode': '',
        'UnitCode': '',
        'Year':'' ,
        'AcefuthorFilter': '',
        'BossCode': '',
        'Fund': '',
        'Level': '',
        'Elite': '',
        'Organization':'' ,
        'Order': 1,
        'Page': page or 1,
        'PageIndex':'' ,
        'ExcludeField':'' ,
        'ZtCode':'' ,
        'Smarts': ''
}
    if title is None and author is None and theme is None and keywd is None:
        print('什么条件都没有,爬不了')
    else:
        result=session.post(url=url,headers=headers,data=data)
        data=json.loads(result.content.decode('utf8'))
        article_list=data['articleList']
        return article_list

def save_data(articles_url):

    articles=[]
    for article_page in articles_url:
        result=requests.get(headers=headers,url=article_page)
        # parsers=HTMLParser()
        # tree=etree.fromstring(result.text,parser=parsers)
        tree = etree.HTML(result.text)

        try:
            responses=tree.xpath("//div[@style='text-align:center; width:660px; height:auto; padding-top: 5px; padding-bottom: 12px;padding-left: 70px;  margin-top: 5px;margin-bottom: 5px']/a[@target='_blank']")
            author=[]
            for response in responses:
                author.append(response.xpath('string(.)'))

            response=tree.xpath("//h1[@class='xx_title']")[0]
            title=response.xpath('string(.)')
            title=title.replace('\n','').replace('\r','').replace('  ','')
            response=tree.xpath("//div[@style='text-align:left;word-break:break-all']")[0]
            content=response.xpath('string(.)').replace('\n','').replace('\r','').replace('  ','')
            # res=etree.tostring(response,encoding='unicode')

            articles.append({"title":title,"author":author,"content":content})
        except:
            print('本文献爬取故障')

    # collection.insert_many(articles)
    try:

        return articles
    except Exception as e:
        print('error:',e)
def cnspider(theme=None,page=None,title=None,author=None,kwd=None):
    articles=[]
    for i in range(1,page+1):
        article_list=find_filename(theme=theme,page=i,title=title,author=author,keywd=kwd)
        articles_url=[]
        index=0
        for article in article_list:

            articles_url.append(get_message(article['fileName']))
        articles+=save_data(articles_url)
    return articles


