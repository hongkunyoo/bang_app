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
        pool = my_threading.MyThreadPool.instance()
        self.my_id = pool.get_id()


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

        b.get(url)
        print('[list] Start: %s' % self.my_id)
        self.find_list(b)

    def find_list(self, b):
        time.sleep(10)
        elements = b.find_elements_by_class_name("Room-item")
        pool = my_threading.MyThreadPool.instance()
        ts = []
        if len(elements) == 0:
            # print('no Room-item!: %s' % self.my_id)
            print('[list] Released: %s' % self.my_id)
            b.quit()
            return
        for el in elements:
            a_tag = el.find_element_by_tag_name("a")
            href = a_tag.get_attribute('href')
            c = crawl_bang.Crawler()
            # c.crawl(href)
            t = pool.submit2(c.crawl, href)
            ts.append(t)

        for t in ts:
            try:
                t.result(timeout=60 * 3)
            except concurrent.futures.TimeoutError:
                t.cancel()
                print('[list] Cancelled: %s' % self.my_id)
                b.quit()
                return

        try:
            next_btn = b.find_element_by_class_name('Pagination-item--next')
        except selenium.common.exceptions.NoSuchElementException:
            print('[list] Released: %s' % self.my_id)
            b.quit()
            return
        time.sleep(2)
        try:
            b.find_element_by_css_selector(".Pagination-item--next.disable")
            print('[list] Released: %s' % self.my_id)
            b.quit()
            return
        except selenium.common.exceptions.NoSuchElementException:
            next_btn.click()
            self.find_list(b)


