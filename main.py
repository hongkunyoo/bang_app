import crawl_list
import crawl_bang
import re
import storage
import my_threading
import concurrent
import my_driver


# (높이, 가로)
# 좌상(37.800000, 126.470000)
# 우상(37.800000, 127.470000)
# 좌하(36.800000, 126.470000)
# 우하(36.800000, 127.470000)


def main():
    count = 0

    cal = 3
    step = int(100/cal)
    lngs = get_lngs(step)
    pool = my_threading.MyThreadPool.instance()
    ts = []

    # c = crawl_list.Crawl(count)
    # t = pool.submit(c.crawl, 37.3, 126.97)
    # ts.append(t)

    for lng in lngs:
        lats = get_lats(step)
        for lat in lats:
            c = crawl_list.Crawl(count)
            t = pool.submit(c.crawl, lng, lat)
            ts.append(t)

            count += 1

    for t in concurrent.futures.as_completed(ts):
        t.result(timeout=2)
    print('done')

    # main3()

# 37
def get_lngs(step=1):
    for i in range(3680, 3780, step):
        yield i/100


# 126
def get_lats(step=1):
    for i in range(12647, 12747, step):
        yield i/100


import concurrent.futures
import urllib.request
import time

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://www.google.com/',
        'http://coffeewhale.com']


# Retrieve a single page and report the url and contents
def load_url(url, timeout):
    print('load url')
    time.sleep(1)
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        print(len(conn.read()))


def main2():
    # We can use a with statement to ensure threads are cleaned up promptly
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    # for future in (future_to_url):
    #     url = future_to_url[future]
    #     try:
    #         data = future.result()
    #     except Exception as exc:
    #         print('%r generated an exception: %s' % (url, exc))
    #     else:
    #         print('%r page is' % url)


def main3():
    s = storage.Storage()
    count = (len([i for i in s.get_entities()]))
    print(count)
    # with open('plz.txt', 'w') as f:
    #     print('total: ', count, file=f)
        # print('insert: ', pool.insert_count, file=f)

import platform
import threading

def main4():

    lat = 126.97
    lng = 37.3

    url = 'https://www.dabangapp.com/search#/map?id=&type=search&filters={"deposit-range":' \
          '[0,999999],"price-range":[0,999999],"room-type":[0,1,2,3,4,5],"deal-type":[0,1]}&position={"center":[%s, %s],"zoom":16}&cluster={}' % (lat, lng)
    ts = []

    def target():
        print('>>>start thread!')
        driver = my_driver.get_driver(platform.system())
        driver.get(url)
        els = driver.find_elements_by_class_name("Room-item")
        for el in els:
            print(el)
        driver.quit()
        print('end thread<<<')

    for i in range(30):
        t = threading.Thread(target=target)
        t.start()
        ts.append(t)
    print('---------------')
    for t in ts:
        t.join()

    print('done')

main()
