#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from six import itervalues
import pymysql
import json
import time

class SQL():
    #数据库初始化
    def __init__(self):
        #数据库连接相关信息
        hosts    = ''       #
        username = ''       #
        password = ''       #   链接数据库配置信息（采集数据库）
        database = 'caiji'  #
        charsets = 'utf8'   #

        self.connection = False
        try:
            self.conn1 = pymysql.connect(host = hosts,user = username,passwd = password,db = database,charset = charsets)
            self.cursor1 = self.conn1.cursor()
            self.cursor1.execute("set names "+charsets)
            self.conn2 = pymysql.connect(host = '',user = '',passwd = '',db = '',charset = '') # 采集数据入文章库
            self.cursor2 = self.conn2.cursor()
            self.cursor2.execute("set names utf8")
            self.connection = True
        except Exception as e:
            print("Cannot Connect To Mysql!/n",e)

    def escape(self,string):
        return '%s' % string
    #插入数据到数据库   
    def insert(self,tablename=None,**values):
        if self.connection: 
            tablename = self.escape(tablename)

            if values:
                # if values['title']:
                #     values['title'] = values['title'].replace('"',"\"")
                # if values['intro']:
                #     values['intro'] = values['intro'].replace('"',"\"")
                # json_values = json.dumps(values,ensure_ascii=False)


                # 采集数据入库语句
                create_table = "Create Table If Not Exists %s(`id` int NOT NULL AUTO_INCREMENT,`title` varchar(60) NOT NULL DEFAULT '' COMMENT '文章标题',`curl` varchar(150) NOT NULL DEFAULT '' COMMENT '原文链接',`intro` varchar(255) NOT NULL DEFAULT '' COMMENT '描述',`thumb` varchar(160) NOT NULL DEFAULT '' COMMENT '缩略图',`settime` int(10) NOT NULL COMMENT '发布时间',`gettime` int(10) NOT NULL COMMENT '采集时间',`style` tinyint(2) unsigned NOT NULL DEFAULT '5' COMMENT '文章类别',`source` varchar(100) NOT NULL DEFAULT '' COMMENT '来源',PRIMARY KEY (`id`),KEY `title` (`title`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8" % tablename
                sql_query = "insert into %s(title,curl,intro,thumb,settime,gettime,style,source) values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (tablename,values['title'],values['url'],values['intro'],values['thumbs'],values['settime'],values['gettime'],values['style'],values['source'])
                if not values['settime']:
                    settime = time.strftime('%Y-%m-%d',time.localtime())
                else:
                    settime = time.strftime("%Y-%m-%d",time.localtime(int(values['settime'])))

                # 采集数据入文章系统语句
                # sql_content = "insert into `表名`(`title`,`link`,`summary`,`image`,`date`,`created`,`menu_id`,`from`) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (values['title'],values['url'],values['intro'],values['thumbs'],settime,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),values['style'],values['source'])
                try:
                    self.cursor1.execute(create_table)
                    self.cursor1.execute(sql_query)
                    self.conn1.commit()
                except Exception as e:
                    print("An Error Occured: ",e)

                try:
                    self.cursor2.execute(sql_content)
                    self.conn2.commit()
                except Exception as e:
                    print("woocms An Error Occured/n",e)

            self.conn1.close()
            self.conn2.close()