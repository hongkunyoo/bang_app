from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import asyncio
import concurrent.futures


PATH_LIST = {
    "Windows": 'phantomjs-windows/bin/phantomjs.exe',
    "Linux": 'phantomjs-linux/bin/phantomjs',
    "Darwin": 'phantomjs-macos/bin/phantomjs'
}


def get_driver(os_system):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
        "(KHTML, like Gecko) Chrome/15.0.87"
    )
    path = PATH_LIST[os_system]
    driver = webdriver.PhantomJS(path, desired_capabilities=dcap)
    # driver = webdriver.Chrome('chromedriver.exe')
    driver.set_window_size(1920, 950)
    driver.implicitly_wait(10)
    return driver


def get_async_driver(os_system):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
        "(KHTML, like Gecko) Chrome/15.0.87"
    )
    path = PATH_LIST[os_system]
    driver = AsyncDriver(path, desired_capabilities=dcap)
    # driver = webdriver.Chrome('chromedriver.exe')
    driver.set_window_size(1920, 950)
    driver.implicitly_wait(10)
    return driver


class AsyncDriver(webdriver.PhantomJS):

    def __init__(self, executable_path="phantomjs", port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS,
                 service_args=None, service_log_path=None):
        super(AsyncDriver, self).__init__(executable_path=executable_path, port=port, desired_capabilities=desired_capabilities,
                 service_args=service_args, service_log_path=service_log_path)

        max_workers = 30

        self. executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix='driver')
        self.loop = asyncio.get_event_loop()

        # for method in dir(self):
        #     if not method.startswith("find"):
        #         continue
        #
        #     new_method = self.define_method(method)
        #     print(method, new_method)
        #     setattr(self, method, new_method)

    # def define_method(self, name):
    #     async def async_method(target, wait=2):
    #         method_to_call = getattr(webdriver.PhantomJS, name)
    #         ret = await self.loop.run_in_executor(self.executor, method_to_call, self, target)
    #         await asyncio.sleep(wait)
    #         return ret
    #     return async_method

    async def get(self, url, wait=2):
        await self.loop.run_in_executor(self.executor, webdriver.PhantomJS.get, self, url)
        await asyncio.sleep(wait)

    async def find_element(self, by, value, wait=2):
        ret = await self.loop.run_in_executor(self.executor, webdriver.PhantomJS.find_element, self, by, value)
        await asyncio.sleep(wait)
        print(AsyncWebElement(ret))
        return AsyncWebElement(ret)

    async def find_elements(self, by, value, wait=2):
        ret = await self.loop.run_in_executor(self.executor, webdriver.PhantomJS.find_elements, self, by, value)
        await asyncio.sleep(wait)

        return list(map(lambda x: AsyncWebElement(x), ret))


class AsyncWebElement(object):

    def __init__(self, webelement):
        self.element = webelement
        max_workers = 30

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix='web_element')
        self.loop = asyncio.get_event_loop()

    async def get_attribute(self, attr, wait=2):
        ret = await self.loop.run_in_executor(self.executor, self.element.get_attribute, attr)
        await asyncio.sleep(wait)
        return ret
