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
import util

by_mapper = {
    "class": By.CLASS_NAME,
    "tag": By.TAG_NAME,
    "id": By.ID,
    "attr": "attr",
    "text": "text"
}


class Crawl(object):

    def __init__(self):
        # threading.Thread.__init__(self)
        self.pool = my_threading.MyThreadPool.instance()

    def crawl(self, lng, lat):
        self.my_id = self.pool.get_id(0)
        # self.f = open('logs/%04d.txt' % self.my_id, 'w')
        self.f = None
        util.my_print('---START crawl list---', file=self.f)
        self.lat = lat
        self.lng = lng
        url = 'https://www.dabangapp.com/search#/map?id=&type=search&' \
              'filters={"deposit-range":[0,999999],"price-range":[0,999999],' \
              '"room-type":[0,1,2,3,4,5],"deal-type":[0,1]}&' \
              'position={"center":[%s, %s],"zoom":16}&cluster={}' % (lat, lng)
        self.url = url
        util.my_print('url: %s' % url, file=self.f)
        self.b = my_driver.get_driver(platform.system())
        return self.run()

    def run(self):
        url = self.url
        b = self.b
        rand = random.randint(2, 10)
        time.sleep(rand)

        b.get(url)
        util.my_print('b.get', file=self.f)
        # print('[list] Start: %s' % self.my_id)
        ts = self.find_list(b, [], 30)
        util.my_print('---END crawl list---', file=self.f)
        self.pool.releas_id(0, self.my_id)
        b.quit()
        util.close_file(self.f)
        return ts

    def find_list(self, b, ts, until):
        util.my_print('start find list', file=self.f)
        if until <= 0:
            util.my_print('[find list] in if until', file=self.f)
            return ts
        time.sleep(10)
        elements = b.find_elements_by_class_name("Room-item")
        pool = my_threading.MyThreadPool.instance()
        # ts = []
        if len(elements) == 0:
            util.my_print('[find list] len(elements)==0', file=self.f)
            # print('no Room-item!: %s' % self.my_id)
            # print('[list] Released: %s' % self.my_id)
            return ts
        util.my_print('[find list] for el in elements', file=self.f)
        for idx, el in enumerate(elements):
            a_tag = el.find_element_by_tag_name("a")
            href = a_tag.get_attribute('href')
            c = crawl_bang.Crawler()
            # c.crawl(href)
            t = pool.submit2(c.crawl, href)
            ts.append(t)
            util.my_print('[find list] %s bang crawl' % idx, file=self.f)

        try:
            next_btn = b.find_element_by_class_name('Pagination-item--next')
        except selenium.common.exceptions.NoSuchElementException:
            # print('[list] Released: %s' % self.my_id)
            util.my_print('[find list] no such next', file=self.f)
            return ts
        time.sleep(2)
        try:
            b.find_element_by_css_selector(".Pagination-item--next.disable")
            # print('[list] Released: %s' % self.my_id)
            util.my_print('[find list] no more next button', file=self.f)
            return ts
        except selenium.common.exceptions.NoSuchElementException:
            next_btn.click()
            return self.find_list(b, ts, until-1)


