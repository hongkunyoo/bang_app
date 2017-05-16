from queue import Queue
import threading
import concurrent.futures
import time
import my_driver
import platform
import sys, traceback


class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        with cls.__singleton_lock:
            if not cls.__singleton_instance:
                cls.__singleton_instance = cls()
        return cls.__singleton_instance


def cancelable(func):
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            ex_type, ex, tb = sys.exc_info()
            traceback.print_tb(tb)
            print('cancelled: ', e)

    return inner_func


# class Crawl:
#
#     def crawl(self, timeout):
#         # url = 'http://hongkunyoo.cloudapp.net:3000/?t=%s' % timeout
#         url = 'https://www.dabangapp.com/room/58fedd8713d7925148dc8945'
#         self.start = time.time()
#         self.driver = my_driver.get_driver(platform.system())
#         # res = requests.request('GET', url)
#         self.driver.get(url)
#         print('crawl: ', time.time() - self.start)
#
#     def cancel(self):
#         self.driver.quit()
#         print('crawl: ', time.time() - self.start)


class MyWorker(threading.Thread):

    def __init__(self, on_run, on_cancel, *args):
        threading.Thread.__init__(self)
        self.daemon = True
        self.on_run = on_run
        self.on_cancel = on_cancel
        self.args = args

    def run(self):

        self.on_run(*self.args)

    def cancel(self):
        self.on_cancel()


class CancelableThread(threading.Thread):

    def __init__(self, q, on_run, on_cancel, wait_until, *args):
        threading.Thread.__init__(self)
        self.wait_until = wait_until
        # self.event = threading.Event()
        self.q = q
        self.worker = MyWorker(on_run, on_cancel, *args)

    def init(self, sema, pool):
        self.sema = sema
        self.pool = pool

    def run(self):
        self.start = time.time()
        self.worker.start()
        self.pool.start(self.ident)
        self.worker.join(self.wait_until)
        if self.worker.isAlive():
            self.worker.cancel()
            print('[%s] Canceled: %s' % (self.ident, time.time() - self.start))
        else:
            print('[%s] Released: %s' % (self.ident, time.time() - self.start))
        # self.event.set()
        self.q.task_done()
        self.sema.release()
        self.pool.release(self.ident)


class ThreadPool(SingletonMixin):

    def __init__(self, num_threads=30):
        self.tasks = []
        self.q = Queue(num_threads)
        self.num_of_thread = num_threads
        self.id_dic = {}
        self.lock = threading.Lock()

    def start(self, ident):
        self.lock.acquire()
        self.id_dic[ident] = 0
        self.lock.release()

    def release(self, ident):
        self.lock.acquire()
        self.id_dic[ident] = 1
        self.lock.release()

    # def get_id(self, _type):
    #     self.id += 1
    #     self.id_dic[_type][self.id] = 0
    #     return self.id
    #
    # def releas_id(self, _type, id):
    #     self.id_dic[_type][id] = 1

    def submit(self, on_run, on_cancel, wait_until, *args):

        on_run = cancelable(on_run)
        # wait = CancelableThread(on_run, on_cancel, *args)
        c = CancelableThread(self.q, on_run, on_cancel, wait_until, *args)
        self.tasks.append(c)
        # self.q.put((on_run, on_cancel, args))

        return c

    def assign_thread(self, event):
        print('start assign thread')
        count = 0
        q = self.q
        tasks = self.tasks,
        s = threading.Semaphore(self.num_of_thread)
        pool = self.instance()
        while not (q.empty() and len(tasks) == 0 and self.is_all_released()):
            s.acquire()
            c = q.get()
            c.init(s, pool)
            count += 1
            c.start()
        event.set()

        print('end assign_thread')

    def join(self):
        event = threading.Event()
        assign_t = threading.Thread(target=self.assign_thread, args=(event, ))
        assign_t.start()
        put_count = 0

        while len(self.tasks) != 0 or not event.isSet():
            if len(self.tasks) == 0:
                time.sleep(5)
                continue
            c = self.tasks.pop(0)
            self.q.put(c)
            put_count += 1
        self.q.join()
        assign_t.join()

    def is_all_released(self):
        return all(v == 1 for v in self.id_dic.values())


def main():
    task_len = 100
    num_threads = 10
    wait_until = 100
    job_time = 3

    pool = ThreadPool(num_threads=num_threads)

    for i in range(task_len):
        # c = Crawl()
        # pool.submit(c.crawl, c.cancel, wait_until)
        print(i)

    print('---START JOIN-----')
    pool.join()
    print('---END   JOIN-----')


# main()
# print('last: ', threading.active_count())


#
#
# from threading import Thread
# class Worker(Thread):
#     """ Thread executing tasks from a given tasks queue """
#     def __init__(self, tasks):
#         Thread.__init__(self)
#         self.tasks = tasks
#         self.daemon = True
#         self.start()
#
#     def run(self):
#         while True:
#             func, args, kargs = self.tasks.get()
#             try:
#                 func(*args, **kargs)
#             except Exception as e:
#                 # An exception happened in this thread
#                 print(e)
#             finally:
#                 # Mark this task as done, whether an exception happened or not
#                 self.tasks.task_done()
#
#
# class ThreadPool:
#     """ Pool of threads consuming tasks from a queue """
#     def __init__(self, num_threads):
#         self.tasks = Queue(num_threads)
#         for _ in range(num_threads):
#             Worker(self.tasks)
#
#     def add_task(self, func, *args, **kargs):
#         """ Add a task to the queue """
#         self.tasks.put((func, args, kargs))
#
#     def map(self, func, args_list):
#         """ Add a list of tasks to the queue """
#         for args in args_list:
#             self.add_task(func, args)
#
#     def wait_completion(self):
#         """ Wait for completion of all the tasks in the queue """
#         self.tasks.join()
#
#
# if __name__ == "__main__":
#     from random import randrange
#     from time import sleep
#
#     # Function to be executed in a thread
#     def wait_delay(d):
#         print("sleeping for (%d)sec" % d)
#         sleep(d)
#
#     # Generate random delays
#     delays = [randrange(3, 7) for i in range(50)]
#
#     # Instantiate a thread pool with 5 worker threads
#     pool = ThreadPool(5)
#
#     # Add the jobs in bulk to the thread pool. Alternatively you could use
#     # `pool.add_task` to add single jobs. The code will block here, which
#     # makes it possible to cancel the thread pool with an exception when
#     # the currently running batch of workers is finished.
#     pool.map(wait_delay, delays)
#     pool.wait_completion()
