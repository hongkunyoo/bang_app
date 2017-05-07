from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
import os, platform
import importlib
import time
import crawl_bang
import threading
import my_threading
import random
import concurrent
import my_driver


by_mapper = {
    "class": By.CLASS_NAME,
    "tag": By.TAG_NAME,
    "id": By.ID,
    "attr": "attr",
    "text": "text"
}


class Crawl(object):

    def __init__(self, count):
        # threading.Thread.__init__(self)
        pass


    def crawl(self, lng, lat):

        self.lat = lat
        self.lng = lng
        # url = 'https://www.dabangapp.com/search#/map?id=11440101&type=region&filters={"deposit-range":[0,999999],"price-range":[0,999999],"room-type":[0,1,2,3,4,5],"deal-type":[0,1]}&position={"center":[%s,%s],"zoom":16}&cluster={}' % (lng, lat)
        url = 'https://www.dabangapp.com/search#/map?id=&type=search&filters={"deposit-range":[0,999999],"price-range":[0,999999],"room-type":[0,1,2,3,4,5],"deal-type":[0,1]}&position={"center":[%s, %s],"zoom":16}&cluster={}' % (lat, lng)
        self.url = url
        self.b = my_driver.get_driver(platform.system())
        self.run()

    def run(self):
        url = self.url
        b = self.b
        rand = random.randint(2, 10)
        time.sleep(rand)
        print('crawl list!: %s' % url)
        b.get(url)
        time.sleep(10)
        # b.save_screenshot('plz.png')
        self.find_list(b)

    def find_list(self, b):
        print('Start finding list')
        elements = b.find_elements_by_class_name("Room-item")
        pool = my_threading.MyThreadPool.instance()
        ts = []
        if len(elements) == 0:
            print('no Room-item!: %s' % self.url)
            b.save_screenshot('png/%s%s.png' % (self.lat, self.lng))
        for el in elements:
            a_tag = el.find_element_by_tag_name("a")
            href = a_tag.get_attribute('href')
            c = crawl_bang.Crawler()
            # c.crawl(href)
            t = pool.submit2(c.crawl, href)
            ts.append(t)

        for t in concurrent.futures.as_completed(ts):
            t.result()

        try:
            next_btn = b.find_element_by_class_name('Pagination-item--next')
        except selenium.common.exceptions.NoSuchElementException:
            b.quit()
            print('released list: %s' % threading.activeCount())
            return
        time.sleep(2)
        try:
            b.find_element_by_css_selector(".Pagination-item--next.disable")
            b.quit()
            print('released list: %s' % threading.activeCount())
            return
        except selenium.common.exceptions.NoSuchElementException:
            next_btn.click()
            time.sleep(10)
            self.find_list(b)


