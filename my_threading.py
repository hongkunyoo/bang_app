import concurrent.futures
import threading
from queue import Queue

class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        with cls.__singleton_lock:
            if not cls.__singleton_instance:
                cls.__singleton_instance = cls()
        return cls.__singleton_instance


class MyThreadPool(SingletonMixin):

    def __init__(self):
        self.id = 0
        self.submit_count1 = 0
        self.submit_count2 = 0
        self.count = 0
        self.insert_count = 0
        self.id_dic = [{},{}]
        self.ts1 = []
        self.ts2 = []
        self.q = Queue()

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        self.executor2 = concurrent.futures.ThreadPoolExecutor(max_workers=20)

    def submit(self, func, *args):
        # print('in submit1: %s' % self.submit_count1)
        # print('active1: %s' % threading.activeCount())
        self.submit_count1 += 1

        t = self.executor.submit(func, *args)
        self.q.put(t)
        # self.ts1.append(t)
        return t

    def submit2(self, func, *args):
        # print('in submit2: %s' % self.submit_count2)
        # print('active2: %s' % threading.activeCount())
        self.submit_count2 += 1

        t = self.executor2.submit(func, *args)
        self.q.put(t)
        # self.ts2.append(t)
        return t

    def incr_count(self):
        self.count += 1

    def incr_insert_count(self):
        self.insert_count += 1

    def get_id(self, _type):
        self.id += 1
        self.id_dic[_type][self.id] = 0
        return self.id

    def releas_id(self, _type, id):
        self.id_dic[_type][id] = 1

    def get_size(self):
        return self.q.qsize()

    def get_item(self):
        return self.q.get()

    def is_empty_Q(self):
        return self.q.empty()