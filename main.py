import crawl_list
import storage
import bang_threading
import concurrent
import threading
import pandas as pd
import time
import argparse
import coffeewhale
import util
import sys

# (lng, lat)
# left_high (37.800000, 126.470000)
# righ_high (37.800000, 127.470000)
# left_low  (36.800000, 126.470000)
# right_low (36.800000, 127.470000)


def check_status(f):
    pool = bang_threading.ThreadPool.instance()
    lock = threading.RLock()
    while True:
        lock.acquire()
        print('======[Thread: %s]=======' % threading.active_count())
        try:
            count_list = 0
            count_bang = 0
            # for i, mydic in enumerate(pool.id_dic):

            for k, v in pool.id_dic.items():
                if v == 0:
                    print('[%04d] Not released' % k)
                # else:
                #     print('[%04d]     Released' % k)
            print('========================')
        except RuntimeError:
            pass
        # f.flush()
        time.sleep(10)
        lock.release()


def main():
    parser = argparse.ArgumentParser(description='bang app')
    parser.add_argument('-c', type=str, default='crawl')
    parser.add_argument('-num', type=int, default=10)

    args = parser.parse_args()
    if args.c == 'crawl':
        crawl(args.num)
    elif args.c == 'dump':
        dump()
    else:
        print_total_len()


# @coffeewhale.alarmable
def crawl(cal):

    step = int(100/cal)
    lngs = get_lngs(step)
    pool = bang_threading.ThreadPool.instance()
    ts = []

    # f = open('logs/0000.txt', 'w')
    # f2 = open('logs/00000.txt', 'w')
    f = None
    # f2 = sys.stdout
    check_t = threading.Thread(target=check_status, args=(f, ))
    wait_until = 60 * 5
    idx = 0
    for lng in lngs:
        lats = get_lats(step)
        for lat in lats:
            c = crawl_list.Crawl()
            # print('crawl c: %s' % idx)
            idx += 1
            pool.submit(c.crawl, c.cancel, wait_until, lng, lat)
            # t = pool.submit(c.crawl, lng, lat)
            # ts.append(t)

    check_t.start()
    pool.join()
    # for t in concurrent.futures.wait(ts, timeout=60):
    # for idx, t in enumerate(pool.get_ts1()):
    # while not pool.is_empty_Q():
    #     try:
    #         t = pool.get_item()
    #         t.result(timeout=60 * 3)
    #         print('***[%04d thread done! (%s)]***' % (idx, pool.get_size()))
    #         # tts = t.result()
    #     except concurrent.futures.TimeoutError as e:
    #         print('[list] Cancelled: %s' % t.cancel())

    # check_t.join(15)
    print('done')
    # f.close()
    # f2.close()


# 37
def get_lngs(step=1):
    for i in range(3680, 3780, step):
        yield i/100


# 126
def get_lats(step=1):
    for i in range(12647, 12747, step):
        yield i/100


def print_total_len():
    s = storage.Storage()
    count = (len([i for i in s.get_entities()]))
    print(count)


def dump():

    s = storage.Storage()
    df = pd.DataFrame([i for i in s.get_entities()])
    df.to_csv('bang.csv', encoding='utf-8', index=False)


main()

