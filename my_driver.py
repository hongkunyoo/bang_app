from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


PATH_LIST = {
    "Windows": 'phantomjs-windows/bin/phantomjs.exe',
    "Linux": 'phantomjs-linux/bin/phantomjs'
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
