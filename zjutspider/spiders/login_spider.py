# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import base64
from PIL import Image
import json
from pathlib import Path


class LoginSpiderSpider(scrapy.Spider):
    name = 'login_spider'
    allowed_domains = ['http://gdjw.zjut.edu.cn']
    start_urls = ['http://www.gdjw.zjut.edu.cn/jwglxt/xtgl/index_initMenu.html']

    def start_requests(self):
        cookie_path = "C:\\pypracticcccc\\scrapydemo\\zjutspider\\cookie.json"
        if not Path(cookie_path).exists():
            self.login_gdjw()

        with open(cookie_path, 'r', encoding='utf-8') as f:
            listcookies = json.loads(f.read())

        cookies_dict = dict()
        for cookie in listcookies:
            # 在保存成dict时，我们其实只要cookies中的name和value，而domain等其他都可以不要
            cookies_dict[cookie['name']] = cookie['value']

        yield scrapy.Request(url="http://www.gdjw.zjut.edu.cn/jwglxt/xtgl/index_initMenu.html", cookies=cookies_dict, callback=self.parse,)

    @staticmethod
    def login_gdjw():
        url = "http://www.gdjw.zjut.edu.cn/jwglxt"
        driver_path = r"C:\Users\20180\Desktop\pachong\chromedriver.exe"

        driver = webdriver.Chrome(executable_path=driver_path)
        driver.get(url)
        while True:
            yhm = driver.find_element_by_id('yhm')
            yhm.send_keys("*****")
            mm = driver.find_element_by_id('mm')
            mm.send_keys('*****')

            yzmPic = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "yzmPic"))
            )
            yzmPic.screenshot("test.png")
            data = ""
            # 将四通道图片转换为三通道
            image = Image.open("C:\\pypracticcccc\\scrapydemo\\zjutspider\\test.png").convert("RGB")
            image.save("C:\\pypracticcccc\\scrapydemo\\zjutspider\\test1.jpg")
            with open("C:\\pypracticcccc\\scrapydemo\\zjutspider\\test1.jpg", 'rb') as fp:
                data = base64.b64encode(fp.read())
            print(data.decode('utf-8'))

            import requests
            formdata = {
                "image": data
            }
            responese = requests.post(url="http://localhost:19952/captcha/v1", data=formdata)
            yzmm = responese.json()['message']
            yzm = driver.find_element_by_id('yzm')
            yzm.send_keys(yzmm)
            dl = driver.find_element_by_id('dl')
            dl.click()

            # 判断是否登陆成功
            current_url = driver.current_url
            # if not current_url.find("login") == -1:
            #     driver.close()
            if current_url.find("login") == -1:
                break
        cookie = driver.get_cookies()
        jsonCookies = json.dumps(cookie)
        with open('C:\\pypracticcccc\\scrapydemo\\zjutspider\\cookie.json', 'w') as f:
            f.write(jsonCookies)

    def parse(self, response):
        if response.url.find("login"):
            self.login_gdjw()
        print("=" * 40)
        print("response text: %s" % response.url)
        print("response headers: %s" % response.headers)
        print("response status: %s" % response.status)
        print("request headers: %s" % response.request.headers)
        print("request cookies: %s" % response.request.cookies)
        print("request meta: %s" % response.request.meta)

