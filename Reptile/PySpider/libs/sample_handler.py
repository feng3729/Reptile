#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on __DATE__
# Project: __PROJECT_NAME__
# style:{
#   社会〖ID：2〗,军情播报〖ID：3〗,汽车资讯〖ID：4〗,游戏影音〖ID：6〗,生活杂谈〖ID：7〗,数码〖ID：8〗
#}

from pyspider.libs.base_handler import *
from lxml import etree
import os
import time
import json

class Handler(BaseHandler):
    crawl_config = {
        'itag':'v0.1'
    }

    @every(minutes=20)
    def on_start(self):
        self.crawl('__START_URL__', callback=self.index_page)

    @config(age=20 * 60)
    def index_page(self, response):
        html = etree.HTML(response.text)
        lists = html.xpath('.//')
        for list in lists:
            url = list.xpath('.//')
            if len(list.xpath('.//'))>0:
                title = list.xpath('.//')[0]
            else:
                title =''
            if len(list.xpath('.//'))>0:
                intro = list.xpath('.//')[0]
            else:
                intro = ''
            if len(list.xpath('.//'))>0:
                thumbs = list.xpath('.//')[0]
            else:
                thumbs = ''
            if len(list.xpath('.//'))>0:
                settime = list.xpath('.//')[0]
            else:
                settime = ''
            if len(url)>0:
                self.crawl(url[0],callback=self.detail_page,save={"title":title,"intro":intro,"thumbs":thumbs,"settime":settime})

    @config(priority=2)
    def detail_page(self, response):
        if len(etree.HTML(response.text).xpath('.//meta[@name="_pubtime"]/@content'))>0:
            settime = etree.HTML(response.text).xpath('.//meta[@name="_pubtime"]/@content')[0]
            settime = int(time.mktime(time.strptime(settime, "%Y-%m-%d %H:%M:%S")))
        else:
            settime = 0
        resultjson = json.dumps({"url":response.url,"title":response.save['title'],"intro":response.save['intro'],"thumbs":response.save['thumbs'],"settime":response.save['settime']},ensure_ascii=False)
        isExists = os.path.exists("/home/pyspider/__PROJECT_NAME__/")
        if not isExists:
            os.makedirs("/home/pyspider/__PROJECT_NAME__")
        with open("/home/pyspider/__PROJECT_NAME__/%s.json" % time.strftime('%Y%m%d',time.localtime()),"a+") as f:
            f.write(resultjson)
            f.close()
        return {
            "title":response.save['title'],
            "url":response.url,
            "intro":response.save['intro'],
            "thumbs":response.save['thumbs'],
            "settime":settime,
            "gettime":time.time(),
            "style":"10",
            "source":""
        }
