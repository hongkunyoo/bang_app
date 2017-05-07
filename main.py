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

    # for t in concurrent.futures.as_completed(ts, timeout=2):
    for t in ts:
        try:
            t.result(timeout=60 * 8)
        except concurrent.futures.TimeoutError:
            t.cancel()
            print('[list] Cancelled: %s' % c.my_id)

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


main()
