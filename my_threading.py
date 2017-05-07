import concurrent.futures
import threading


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
        self.submit_count = 0
        self.count = 0
        self.insert_count = 0
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        self.executor2 = concurrent.futures.ThreadPoolExecutor(max_workers=20)
        print('<<<<my Thread instatiate!>>>>')

    def submit(self, func, *args):
        # print('in submit: %s' % self.count)
        # print('active: %s' % threading.activeCount())
        self.submit_count += 1

        return self.executor.submit(func, *args)

    def submit2(self, func, *args):
        self.submit_count += 1

        return self.executor2.submit(func, *args)

    def incr_count(self):
        self.count += 1

    def incr_insert_count(self):
        self.insert_count += 1
