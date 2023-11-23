import scrapy
from selenium import webdriver
import re
import string
import random
import time
import json
from segmentfaultspider.items import SegmentfaultspiderItem

class UserspiderSpider(scrapy.Spider):
    name = 'userspider'
    # allowed_domains = ['https://juejin.cn/hot/authors/6809637769959178254']
    start_urls = [
                  'https://juejin.cn/hot/authors/6809635626879549454',
                  'https://juejin.cn/hot/authors/6809637773935378440',
                  'https://juejin.cn/hot/authors/6809637771511070734',
                  'https://juejin.cn/hot/authors/6809637776263217160',
                  'https://juejin.cn/hot/authors/6809637772874219534'
                  ]

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        self.bro=webdriver.Chrome(chrome_options=options)

    def parse(self, response):
        name_list = response.xpath('//div[@class="hot-list"]/a/@href').extract()
        # print(name_list)
        for name in name_list:
            detail_url = "https://juejin.cn" + name
            # print(detail_url)
            yield scrapy.Request(detail_url, callback=self.parse_detail)
            id = name.split("/")[-1]
            # print(id)
            yield scrapy.Request(detail_url,callback=self.parse_follow,meta={'id':id},dont_filter=True)
        # detail_url = "https://juejin.cn" + name_list[0]
        # yield scrapy.Request(detail_url, callback=self.parse_detail)

    def parse_detail(self,response):
        # print(response.text)
        # with open("tmp.html", 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        newitem=SegmentfaultspiderItem()
        newitem['name']=response.xpath('//span[@class="user-name"]/text()')[0].extract()
        if len(response.xpath('//div[@class="block-body"]//span[@class="count"]').extract())==3:
            newitem['up']=response.xpath('//div[@class="block-body"]//span[@class="count"]/text()')[0].extract().replace(',', '')
            newitem['read']=response.xpath('//div[@class="block-body"]//span[@class="count"]/text()')[1].extract().replace(',', '')
            newitem['reputation']=response.xpath('//div[@class="block-body"]//span[@class="count"]/text()')[2].extract().replace(',', '')
        else:
            if len(response.xpath('//div[@class="block-body"]//span[@class="count"]').extract())==2:
                newitem['up'] = "-1"
                newitem['read'] = response.xpath('//div[@class="block-body"]//span[@class="count"]/text()')[0].extract().replace(',', '')
                newitem['reputation'] = response.xpath('//div[@class="block-body"]//span[@class="count"]/text()')[1].extract().replace(',', '')
            else:
                newitem['up']="-1"
                newitem['read'] = "-1"
                newitem['reputation'] = "-1"
        newitem['time']=response.xpath('//div[@class="item-count"]/time/text()')[0].extract().replace('\n', '').replace(' ', '')
        newitem['Afollow']=response.xpath('//div[@class="follow-block block shadow"]//div[@class="item-count"]/text()')[0].extract().replace('\n', '').replace(' ', '').replace(',', '')
        newitem['followA']=response.xpath('//div[@class="follow-block block shadow"]//div[@class="item-count"]/text()')[1].extract().replace('\n', '').replace(' ', '').replace(',', '')
        if len(response.xpath('//div[@class="position"]').extract())==0:
            newitem['loc'] = ""
            newitem['company'] = ""
        else:
            newitem['loc']=response.xpath('//div[@class="position"]/span/node()[1]')[0].extract()
            if newitem['loc']!='<!---->':
                newitem['loc']=response.xpath('//div[@class="position"]/span/node()[1]/text()')[0].extract()
            else:
                newitem['loc']=""
            newitem['company'] = response.xpath('//div[@class="position"]/span/node()[5]')[0].extract()
            if newitem['company']!='<!---->':
                newitem['company']=response.xpath('//div[@class="position"]/span/node()[5]/text()')[0].extract()
            else:
                newitem['company']=""
        if len(response.xpath('//div[@class="intro"]//span[@class="content"]/text()').extract())!=0:
            newitem['introduce']=response.xpath('//div[@class="intro"]//span[@class="content"]/text()')[0].extract().replace('\n', '')
        else:
            newitem['introduce']=""
        print(newitem)
        yield newitem
        # dic={
        #     'name':name,
        #     'up':up,
        #     'read':read,
        #     'reputaion':reputaion,
        #     'time':time,
        #     'followA':followA,
        #     'Afollow':Afollow,
        #     'loc':loc,
        #     'company':company,
        #     'introduce':introduce,
        # }
        # print(dic)

    def parse_follow(self, response):
        # print(response.meta['id'])
        follownum=int(response.xpath('//div[@class="follow-block block shadow"]//div[@class="item-count"]/text()')[1].extract().replace('\n', '').replace(' ', '').replace(',', ''))
        i=0
        while i<follownum:
            url="https://api.juejin.cn/user_api/v1/follow/followers?aid=2608&uuid=7208838064973252151&spider=0&user_id="+str(response.meta['id'])+"&cursor="+str(i)+"&limit=20"
            time.sleep(random.randint(1,4))
            yield scrapy.Request(url, callback=self.parse_json)
            i+=20

    def parse_json(self,response):
        # print(response)
        results = response.text
        pattern=r'"user_id":"(.*?)","user_name"'
        ids=re.findall(pattern,results)
        # print(ids)
        for id in ids:
            url="https://juejin.cn/user/"+id
            yield scrapy.Request(url, callback=self.parse_detail)
        # results = response.json()
        # print(results['data'][)
