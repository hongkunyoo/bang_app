from queue import Queue
import threading
import requests
import time
import my_driver
import platform


def cancelable(func):
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print('cancelled: ', e)

    return inner_func


class Crawl:

    def crawl(self, timeout):
        url = 'http://hongkunyoo.cloudapp.net:3000/?t=%s' % timeout
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
        print('start thread: %s' % self.ident)
        self.on_run(*self.args)

    def cancel(self):
        self.on_cancel()


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


class ThreadPool(object):

    def __init__(self, num_threads):
        self.q = Queue(num_threads)
        self.ts = []

    def submit(self, on_run, on_cancel, *args):
        on_run = cancelable(on_run)
        wait = CancelableThread(on_run, on_cancel, *args)
        wait.start()
        self.ts.append(wait)
        return wait


pool = ThreadPool(num_threads=4)
c = Crawl()
w = pool.submit(c.crawl, c.cancel, 5, (7, ))
print(threading.active_count())
print(w.isAlive())

time.sleep(8)
print('------------------')
print('last: ', threading.active_count())
print('last isAlive: ', w.isAlive())