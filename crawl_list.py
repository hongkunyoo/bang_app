from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
import os, platform
import importlib
import time
import crawl_bang
import threading

PATH_LIST = {
    "Windows": 'phantomjs-windows/bin/phantomjs.exe',
    "Linux": 'phantomjs-linux/bin/phantomjs'
}
by_mapper = {
    "class": By.CLASS_NAME,
    "tag": By.TAG_NAME,
    "id": By.ID,
    "attr": "attr",
    "text": "text"
}


class Crawl(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        PHANTOM_PATH = PATH_LIST[platform.system()]
        self.b = webdriver.PhantomJS(PHANTOM_PATH)
        self.b.implicitly_wait(10)

    def crawl(self, lng, lat):

        url = 'https://www.dabangapp.com/search#/map?id=11440101&type=region&filters={"deposit-range":[0,999999],"price-range":[0,999999],"room-type":[0,1,2,3,4,5],"deal-type":[0,1]}&position={"center":[%s,%s],"zoom":16}&cluster={}' % (lng, lat)
        self.url = url
        self.start()

    def run(self):
        url = self.url
        b = self.b
        b.get(url)
        time.sleep(2)
        self.find_list(b)

    def find_list(self, b):
        elements = b.find_elements_by_class_name("Room-item")

        for el in elements:
            a_tag = el.find_element_by_tag_name("a")
            href = a_tag.get_attribute('href')
            c = crawl_bang.Crawler()
            c.crawl(href)

        next_btn = b.find_element_by_class_name('Pagination-item--next')
        try:
            next_btn_disable = b.find_element_by_css_selector(".Pagination-item--next.disable")
        except selenium.common.exceptions.NoSuchElementException:
            next_btn.click()
            time.sleep(2)
            self.find_list(b)


