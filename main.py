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


def check_status(f):
    pool = my_threading.MyThreadPool.instance()
    lock = threading.RLock()
    while True:
        lock.acquire()
        print('======[Thread: %s]=======' % threading.active_count())
        print('======[Thread: %s]=======' % threading.active_count(), file=f)
        for i, mydic in enumerate(pool.id_dic):
            print('-----[%s]-----' % ("list" if i == 0 else "bang"))
            print('-----[%s]-----' % ("list" if i == 0 else "bang"), file=f)
            for k, v in mydic.items():
                if v == 0:
                    print('[%04d] Not released' % k)
                    print('[%04d] Not released' % k, file=f)
                # else:
                #     print('[%04d]     Released' % k)
        print('========================')
        print('========================', file=f)
        f.flush()
        time.sleep(10)
        lock.release()


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
    f = open('logs/0000.txt', 'w')
    check_t = threading.Thread(target=check_status, args=(f, ))

    for lng in lngs:
        lats = get_lats(step)
        for lat in lats:
            c = crawl_list.Crawl(count)
            t = pool.submit(c.crawl, lng, lat)
            ts.append(t)

            count += 1
    check_t.start()
    # for t in concurrent.futures.wait(ts, timeout=60):
    for idx, t in enumerate(pool.get_ts()):
        try:
            t.result(timeout=60 * 3)
            print('***[%04d thread done! (%s)]***' % (idx, len(pool.get_ts())))
            print('***[%04d thread done! (%s)]***' % (idx, len(pool.get_ts())), file=f)
            # tts = t.result()
        except concurrent.futures.TimeoutError as e:
            print('[list] Cancelled: %s' % t.cancel())
            print('[list] Cancelled: %s' % t.cancel(), file=f)

    check_t.join(15)
    print('done')
    print('done', file=f)
    f.close()


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
