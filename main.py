import crawl_list
import crawl_bang
import re
import storage


# (높이, 가로)
# 좌상(37.800000, 126.470000)
# 우상(37.800000, 127.470000)
# 좌하(36.800000, 126.470000)
# 우하(36.800000, 127.470000)


# def main():
#     count = 0
#     step = 20
#     lngs = get_lngs(step)
#     for lng in lngs:
#         lats = get_lats(step)
#         for lat in lats:
#             c = crawl_list.Crawl()
#             c.crawl(lng, lat)
#             count += 1
#     print(count)


# 37
def get_lngs(step=1):
    for i in range(3680, 3780, step):
        yield i/100


# 126
def get_lats(step=1):
    for i in range(12647, 12747, step):
        yield i/100


def main():
    s = storage.Storage()
    for i in s.get_entities():
        print(i)


main()