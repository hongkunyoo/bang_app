from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import os, platform
import threading
import time
import importlib
import random
import re
import json
import pprint
import storage
import my_threading
import my_driver
import urllib
import util
import sys


by_mapper = {
    "class": By.CLASS_NAME,
    "tag": By.TAG_NAME,
    "id": By.ID,
    "attr": "attr",
    "text": "text"
}


class Crawler(object):

    def __init__(self):
        pass
        # threading.Thread.__init__(self)
        self.pool = my_threading.MyThreadPool.instance()

    def crawl(self, url):
        self.my_id = self.pool.get_id(1)
        # self.f = open('logs/%04d.txt' % self.my_id, 'w')
        self.f = None
        util.print('---START crawl bang---', file=self.f)
        self.url = url
        self.b = my_driver.get_driver(platform.system())
        self.run()

    def run(self):
        rand = random.randint(2, 10)
        time.sleep(rand)
        url = self.url
        util.my_print('url: %s' % url, file=self.f)
        b = self.b
        b.get(url)
        util.my_print('b.get', file=self.f)

        time.sleep(3)
        scripts = b.find_elements_by_tag_name('script')

        def find_until(until, _script):
            util.my_print('start find until', file=self.f)
            if until <= 0:
                util.my_print('[find bang] in if until', file=self.f)
                return ""
            time.sleep(3)
            try:
                innerHTML = _script.get_attribute('innerHTML')
                util.my_print('[find bang] innerHTML', file=self.f)
                return innerHTML
            except Exception:
                return find_until(until-1, _script)

        res = None
        for script in scripts:
            try:
                innerHTML = find_until(3, script)
            except:
                # print(self.url)
                continue

            if "dabang.web.detail" not in innerHTML:
                continue
            util.my_print('[bang] ***find script!***', file=self.f)
            my_json = re.findall(r'dabang.web.detail\((.*)\);', innerHTML)[0]
            my_json = ",".join(my_json.split(',')[:-1])
            j = json.loads(my_json)
            room = j['room']

            fields = [
                'id', 'seq', 'building_floor', 'building_floor_str', 'room_floor', 'floor', 'deal_type', 'deposit',
                'price','elevator','heating','heating_type','jibun_address','road_address','detail_address',
                'maintenance','maintenance_cost','animal','parking','parking_cost','provision_size','room_size',
                'room_type','room_type_str','actived_time','selling_type','status'
            ]
            bang = dict()
            for f in fields:
                bang[f] = room[f]
            bang['location_lng'] = room['location'][0]
            bang['location_lat'] = room['location'][1]
            bang['option'] = ','.join(map(str, room['room_options']))

            bang['PartitionKey'] = str(bang['id'])
            bang['RowKey'] = str(bang['seq'])

            # pool = my_threading.MyThreadPool.instance()
            # pool.incr_count()
            store = storage.Storage()
            res = store.insert(bang)
            util.my_print('[%s] %s' % ("duplicated" if res is None else "success", url), file=self.f)
            break

        util.my_print('[bang] Released: %s (%s)' % (self.my_id, ("duplicated" if res is None else "success", url)))
        self.pool.releas_id(1, self.my_id)
        b.quit()
        util.my_print('---END crawl bang---', file=self.f)
        util.close_file(self.f)

        return
