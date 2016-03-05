# -*- coding: UTF-8 -*-
import urllib

__author__ = 'bohaohan'
import requests
import time
from BeautifulSoup import BeautifulSoup as bs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver

logos = ['Acura','Armani','AstonMartin','Audi','AZIMUT','Balenciaga',
         'Bally','Beneteau','Bentley','Benz','Biotherm','Blumarine','BMW',
         'Bombardier','Bottega Veneta','Braastad','Bucherer','Bulgari',
         'BURBERRY','Cartier','Celine','Cessna','CHANEL','Chevrolet',
         'Chopard','Cirrus','CK','Coach','Constant','Damiani','De Beers',
         'Dior','DKNY','Estee Lauder','Feadship','Fendi','Ferragamo','Ferrari',
         'Franck Muller','Furla','Galtiscopio','Givenchy','Glashutte','GUCCI','GUESS',
         'Gulfstream','hamilton','HERMES','Hublot','Infiniti','IWC','Jaeger',
         'Jaguar','Jeanneau','Lafite','Lamborghini','Lancome','Landrover','Lexus',
         'Longines','LOTOS','LV','Martell','Maserati','Mclaren','MIDO','Mikimoto',
         'Milus','MiuMiu','Montblanc','Nina Ricci','OMEGA','Panerai',
         'PatekPhilippe','Piaget','Pomellato','Porsche','PRADA','Rado',
         'RaymondWeil','Raytheon','Rolex','Rollsroyce','Swarovski','TAG Heuer',
         'Tiffany','Tissot','Titoni','TSL','VanCleefArpels','VeraWang','Volvo',
         'Wally','YSL']
js = "window.scrollTo(0,document.body.scrollHeight)"
num = 0

def spider():
    print "start!"
    pwd = "/Users/bohaohan/iss/商务智能/code/img/"
    tail = ".png"
    url = "http://www.yeslux.com/pinpai.html"
    r = requests.get(url)
    r.encoding = 'gb2312'
    with open(pwd+"a"+tail, 'wb') as fd:
        for chunk in r.iter_content():
                fd.write(chunk)
    root = bs(r.text)
    div = root.find("div", attrs={'class': 'brand_main'})
    lis = div.findAll("li")
    for li in lis:
        img = li.find('img')
        name = img.get("alt")
        src = img.get("src")
        ir = requests.get(src, stream=True)
        with open(pwd+name+tail, 'wb') as fd:
            for chunk in ir.iter_content():
                    fd.write(chunk)
        print name, src, "has been downloaded"
    print "finished!"

def parse(name, browser):

    pwd = "/Users/bohaohan/iss/商务智能/code/mining_data/"
    tail = ".jpg"
    search_name = name + ' logo'
    browser.find_element_by_id('kw').clear()
    browser.find_element_by_id('kw').send_keys(search_name)
    browser.find_element_by_css_selector('.s_btn_wr input').click()
    time.sleep(3)
    for i in range(8):
        browser.execute_script(js)
        time.sleep(3)
    div = browser.find_element_by_id('imgContainer')
    imgs = div.find_elements_by_tag_name('img')
    c = 0
    for img in imgs:
        src = img.get_attribute('src')
        print src, ' Downloading'
        # ir = requests.get(src, stream=True)
        # time.sleep(1)
        file_name = name + '_' + str(c)
        c += 1
        download_img(pwd+file_name+tail, src)
        # with open(pwd+file_name+tail, 'wb') as fd:
        #     for chunk in ir.iter_content():
        #             fd.write(chunk)
        # print src, ' Finish'

def download_img(path, url):
    try:
        ir = requests.get(url, stream=True, headers={
            'User-Agent': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36"
        })
        with open(path, 'wb') as fd:
            for chunk in ir.iter_content():
                    fd.write(chunk)
        # conn = urllib.urlopen(url)
        # f = open(path, 'wb')
        # f.write(conn.read())
        # f.close()
        print url, ' Finish'
    except:
        print url, 'error'


def spider_logo(browser):
    i = 0
    for logo in logos:
        if i > 16:
            parse(logo, browser)
        i += 1


if __name__ == '__main__':
    # url = 'http://img1.imgtn.bdimg.com/it/u=76990598,2986468277&fm=21&gp=0.jpg'
    # img_file=urllib.urlopen(url)
    # r = requests.get(url, headers={
    #     'User-Agent': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36"
    # })
    # print r.content
    browser = webdriver.Firefox()
    url = 'http://image.baidu.com/'
    browser.get(url)
    # browser.
    time.sleep(3)
    # parse('aa logo', browser)
    spider_logo(browser)
