from selenium import webdriver
from WebAuto.common.data_handle import DataHandle,driver_dir



class UnSupportBrowserTypeError(Exception):
    pass


class Browser(object):
    """
       定义一个浏览器引擎类，根据browser_type的值去，控制启动不同的浏览器，这里主要是IE，Firefox, Chrome
    """

    def __init__(self):
        """
        初始化，判断浏览器类型是否可支持，设置driver为None
        """
        self.driver=None
        self.project=None
        self.project_info=None



    def lanuch(self,project,url_suffix="",implicitly_wait=20):
        """
        打开浏览器和网址，设置全局时延，最大化窗口
        :param url:
        :param implicitly_wait:
        :return:
        """
        self.project = project
        self.project_info = DataHandle().obtain_project_info(self.project)

        launch_info=self.project_info[0]
        browser_type = launch_info["driver"]
        if browser_type not in launch_info["driver_types"]:
            raise UnSupportBrowserTypeError("不支持的浏览器类型{0}，目前仅支持{1}".format(browser_type,launch_info["driver_types"]))
        url=launch_info["url"]+url_suffix

        if browser_type=="Phantomjs":
            # phantomjs：无需浏览器的 Web 测试、页面访问自动、屏幕捕获、网络监控
            self.driver = webdriver.PhantomJS(executable_path=driver_dir+"phantomjs.exe")
        elif browser_type=="Chrome":
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument('disable-infobars')
            self.driver=webdriver.Chrome(executable_path=driver_dir+"chromedriver.exe",options=chrome_options)
        elif browser_type=="IE":
            self.driver = webdriver.Ie(executable_path=driver_dir+"IEDriverServer.exe")
        elif browser_type=="Firefox":
            self.driver = webdriver.Firefox(executable_path=driver_dir + "geckodriver.exe")
        elif browser_type=="Chrome_headless":
            # chrome headless:无界面测试
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(executable_path=driver_dir+"chromedriver.exe",options=chrome_options)
            self.driver.set_window_size(1280, 1024)
        self.driver.maximize_window()
        self.driver.implicitly_wait(implicitly_wait)
        self.driver.get(url)
        # cookie = {'domain': 'legal.strategy.aegis-info.com', 'expiry': 1519439710.631926, 'httpOnly': False, 'name': 'user', 'path': '/', 'secure': False, 'value': '"2|1:0|10:1516847686|4:user|8:anNneQ==|383a0a6d445fa2997970a80a68bba0ff83f1f828589ac54f05c2c198e83cf6e1"'}
        # self.driver.add_cookie(cookie)
        # self.driver.refresh()
        # self.driver.get(url)
        # print(self.driver.get_cookies())
        print('web自动化测试网址：' + url)
        return self















