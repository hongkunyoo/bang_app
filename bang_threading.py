from queue import Queue
import threading
import concurrent.futures
import time
import my_driver
import platform


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
            print('cancelled: ', e)

    return inner_func


class Crawl:

    def crawl(self, timeout):
        # url = 'http://hongkunyoo.cloudapp.net:3000/?t=%s' % timeout
        url = 'https://www.dabangapp.com/room/58fedd8713d7925148dc8945'
        self.driver = my_driver.get_driver(platform.system())
        # res = requests.request('GET', url)
        self.driver.get(url)
        print(self.driver.current_url)

    def cancel(self):
        self.driver.quit()


class MyWorker(threading.Thread):

    def __init__(self, on_run, on_cancel, *args):
        threading.Thread.__init__(self)
        self.daemon = True
        self.on_run = on_run
        self.on_cancel = on_cancel
        self.args = args

    def run(self):
        self.start = time.time()
        # print('start run: ', self.start)
        # print('start thread: %s' % self.ident)
        self.on_run(*self.args)
        print('elpase: ', time.time() - self.start)

    def cancel(self):
        self.on_cancel()
        print('elpase: ', time.time() - self.start)


class CancelableThread(threading.Thread):

    def __init__(self, on_run, on_cancel, wait_until, *args):
        threading.Thread.__init__(self)
        self.wait_until = wait_until
        self.worker = MyWorker(on_run, on_cancel, *args)

    def run(self):
        self.worker.start()
        self.worker.join(self.wait_until)
        if self.worker.isAlive():
            self.worker.cancel()


class ThreadPool(SingletonMixin):

    def __init__(self, num_threads):
        self.tasks = []
        self.ts = []
        self.q = Queue(num_threads)

    def submit(self, on_run, on_cancel, wait_until, *args):

        on_run = cancelable(on_run)
        # wait = CancelableThread(on_run, on_cancel, *args)
        c = CancelableThread(on_run, on_cancel, wait_until, *args)
        self.tasks.append(c)
        # self.q.put((on_run, on_cancel, args))

        # wait.start()
        # self.ts.append(wait)
        # return wait
        return None

    def assign_thread(self):
        print('start assign thread')
        while not (self.q.empty() and len(self.tasks) == 0):
            c = self.q.get()
            c.start()
            self.ts.append(c)

        for t in self.ts:
            t.join()
        print('end assign_thread')

    def join(self):
        assign_t = threading.Thread(target=self.assign_thread)
        assign_t.start()

        while len(self.tasks) != 0:
            t = self.tasks.pop(0)
            self.q.put(t)

        assign_t.join()



def main():
    task_len = 40
    num_threads = 4
    wait_until = 1200
    job_time = 3

    pool = ThreadPool(num_threads=num_threads)

    for i in range(task_len):
        c = Crawl()
        pool.submit(c.crawl, c.cancel, wait_until, (job_time, ))
        print(i)

    print('---START JOIN-----')
    pool.join()
    print('---END   JOIN-----')


main()
print('last: ', threading.active_count())
