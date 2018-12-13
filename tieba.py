# -*- coding:utf-8 -*-
#import urllib.request
#import urllib.error
import re,os,traceback
import requests
from io import BytesIO
#from PIL import Image
#from multiprocessing import Pool,cpu_count,freeze_support
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver import Firefox
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.support import expected_conditions as expected
#from selenium.webdriver.support.wait import WebDriverWait
#
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys

class Tool:
    #替换工具
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()

class BDTB:

    def __init__(self, baseUrl, seeLZ, floorTag):
        #初始化输入
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()
        self.files = None
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        self.floorTag = floorTag

    def getpage(self, pageNum):
        #获取贴吧页面
        url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
        headers={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",'Referer':'http://manhua.dmzj.com/tags/s.shtml'}
        try:
            response = requests.get(url,headers=headers).text
        except ConnectionError:
            print('tieba connect fail')
            traceback.print_exc()
            raise ConnectionError
            #response = urllib.request.urlopen(url)
            #request = urllib.request.urlopen(url)
            #response = urllib.urlopen(request)
            #print response.read()
        return response

#        except urllib.error.URLError as e:
##        except urllib3.URLError as e:
#            if hasattr(e, "reason"):
#                print (u"连接百度贴吧失败，错误原因", e.reason)

#    def headless_get(self,pageNum):
#        url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
#        chrome_options = webdriver.ChromeOptions()
#        prefs = {"profile.managed_default_content_settings.images": 2}
#        chrome_options.add_experimental_option("prefs", prefs)
#        driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)
#        driver.get(url)
#        text=driver.page_source
#        print(text)
#        contents = self.getContent(text)
#        driver.quit()
#        return contents
#


    def getTitle(self, page):
        #获取标题
        #page = self.getpage()
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, page):
            #获取页数
            #page = self.getpage()
        pattern = re.compile('<span class="red">(.*?)</span>', re.S)
        #pattern='<span class="red">(.*?)</span>'
        #print(page)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self, page):
        #获取内容
        #page = self.getpage()
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        p = Tool()
        for item in items:
            content = "\n"+ p.replace(item)+"\n"
            contents.append(content)
        return contents

    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + ".txt" ,"w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")

    def writeData(self, contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + "------------------------------------------------ \n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getpage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print ("URL无效，请重试")
            return
        try:
            print (u"该帖子共有" + str(pageNum) + u"页")
            for i in range(1, int(pageNum)+1):
                print ("正在写入第" + str(i) + "页数据")
#                page = self.headless_get(i)
                if i == 1:
                    page=indexPage
                else:
                    page=self.getpage(i)
                contents = self.getContent(page)
                self.writeData(contents)
#                self.writeData(page)
        except IOError as e :
            print ("写入异常，原因"+ e.message)
        finally:
            print ("写入任务完成")
            self.file.close()


print ("请输入帖子代号")
baseURL = 'http://tieba.baidu.com/p/' + str(input(u'http://tieba.baidu.com/p/'))
seeLZ = input("是否只看楼主，是请输入1\n")
floorTag = input("是否写入楼层信息，是输入1\n")
bdtb = BDTB(baseURL,seeLZ,floorTag)
bdtb.start()


















