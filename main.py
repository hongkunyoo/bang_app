import crawl_list
import crawl_bang
import re
import storage
import my_threading
import concurrent
import my_driver
import platform
import threading
import pandas as pd
import time

# (높이, 가로)
# 좌상(37.800000, 126.470000)
# 우상(37.800000, 127.470000)
# 좌하(36.800000, 126.470000)
# 우하(36.800000, 127.470000)


def check_status():
    pool = my_threading.MyThreadPool.instance()
    while True:

        print('======[Thread: %s]=======' % threading.active_count())
        for i, mydic in enumerate(pool.id_dic):
            print('-----[%s]-----' % ("list" if i == 0 else "bang"))
            for k, v in mydic.items():
                if v == 0:
                    print('[%04d] Not released' % k)
                else:
                    print('[%04d]     Released' % k)
        print('========================')
        time.sleep(10)


def main():
    count = 0

    cal = 10
    step = int(100/cal)
    lngs = get_lngs(step)
    pool = my_threading.MyThreadPool.instance()
    ts = []

    # c = crawl_list.Crawl(count)
    # t = pool.submit(c.crawl, 37.3, 126.97)
    # ts.append(t)
    check_t = threading.Thread(target=check_status)

    for lng in lngs:
        lats = get_lats(step)
        for lat in lats:
            c = crawl_list.Crawl(count)
            t = pool.submit(c.crawl, lng, lat)
            ts.append(t)

            count += 1
    check_t.start()
    # for t in concurrent.futures.as_completed(ts, timeout=2):
    for t in ts:
        try:
            tts = t.result(timeout=60 * 8)

            for tt in tts:
                tt.result(timeout=60 * 5)
        except concurrent.futures.TimeoutError:
            t.cancel()
            print('[list] Cancelled: %s' % c.my_id)

    check_t.join(15)
    print('done')


# 37
def get_lngs(step=1):
    for i in range(3680, 3780, step):
        yield i/100


# 126
def get_lats(step=1):
    for i in range(12647, 12747, step):
        yield i/100

def main3():
    s = storage.Storage()
    count = (len([i for i in s.get_entities()]))
    print(count)
    # with open('plz.txt', 'w') as f:
    #     print('total: ', count, file=f)
        # print('insert: ', pool.insert_count, file=f)


def main4():

    s = storage.Storage()
    df = pd.DataFrame([i for i in s.get_entities()])
    df.to_csv('bang.csv', encoding='utf-8', index=False)


main()
