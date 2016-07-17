#coding:utf-8
from selenium import webdriver
import time
import random
from bs4 import BeautifulSoup
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
data=[]
driver= webdriver.PhantomJS()#PhantomJS()#(executable_path='/usr/local/bin/phantomjs')
driver.get('http://waimai.baidu.com/waimai/shoplist/a4838d1f33c94a81')
time.sleep(random.randrange(1,10)*0.1)



#elem=driver.find_elements_by_xpath('//*[@id="shop-list"]/div/div[1]/ul')
elem=driver.find_elements_by_xpath('//li[@data]')
for i in elem:
    data.append(i.text)
#print data[0]
#print data[1]
print data

elem=driver.page_source

driver.quit()

'''

#上面是phantomjs写法,不好用还占用资源,留下来瞻仰另外一种用法



def shop_list(start_page,end_page):
    shop_ids=[]
    saled_month=[]
    average_score=[]
    for i in range(start_page,end_page+1):
        url='http://waimai.baidu.com/waimai/shoplist/59021428a4a7f2ce?display=json&page='+str(i)+'&count=40'
        website=requests.get(url)
        soup=BeautifulSoup(website.text,'lxml')
        #text=str(soup.find_all('script')[-1])
        #print re.findall('"release_id":"(.*?)"',text)
        shop_ids=re.findall('"shop_id":"(.*?)"',str(soup))+shop_ids
        saled_month = re.findall('"saled_month":(.*?),', str(soup)) + saled_month
        average_score=re.findall('"average_score":(.*?),',str(soup))+average_score

    return shop_ids,saled_month,average_score


def start(start_page,end_page):
    counts=1
    tuple=shop_list(start_page,end_page)
    for i in tuple[0]:
        url='http://waimai.baidu.com/waimai/shop/'+i
        headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        website=requests.get(url,headers=headers)
        time.sleep(0.1)
        website.encoding='utf-8'
        soup=BeautifulSoup(website.text,'lxml')
        title=soup.select('#content > div > section.basicinfo > div.b-info.fl > div.one-line > h2')[0].get_text()
        starting_fee=soup.select('#content > div > section.basicinfo > div.b-price.fr > div > strong')[0].get_text()
        deliver_fee=soup.select('#content > div > section.basicinfo > div.b-cost.fr > div')[0].get_text()
        sales_promotion=soup.select('#premium-notice')[0]
        sales_promotions=str([i for i in sales_promotion.stripped_strings]).replace('u\'','\'').decode('unicode-escape')
        f.write(title+'|'+str(tuple[1][counts-1])+'|'+str(tuple[2][counts-1])+'|'+starting_fee+'|'+deliver_fee+'|'+sales_promotions+'|'+url+'\n')
        print '正在写入第%s条餐厅数据'%counts
        counts+=1


if __name__ == '__main__':

    f=open('我周围的外卖'+str(time.ctime())+'.txt','w')
    f.write('餐厅名称|30天销量|好评率|起送费|配送费|促销活动|网址\n')

    a=time.time()
    try:
        start(int(raw_input('请输入起始页数:')),int(raw_input('请输入结束页数:')))
    except AttributeError:
        print 'Error!'
        print '请从新输入'
        start(int(raw_input('请输入起始页数:')),int(raw_input('请输入结束页数:')))
    finally:

        f.close()
    print '数据爬取完毕!'
    print '总用时%.2fs'%(time.time()-a)



    #menu_1 > div.list.clearfix > ul > li:nth-child(2) > div.info.fl > h3
    #menu_2 > div.list.clearfix > ul > li:nth-child(2) > div.info.fl > h3
    #MapHolder > div.mapTopCtrl.BMap_noprint.anchorTR