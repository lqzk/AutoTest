from appium import webdriver
from AppAuto.common.data_handle import DataHandle


class App(object):
    def __init__(self):
        self.driver=None

    def launch(self,project):
        print("测试项目：{0}".format(project))
        desired_caps = DataHandle().obtain_lanuch_parm(project)
        self.driver=webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
        print("[lanuch]成功连接手机和获得对应测试对象")
        return self

