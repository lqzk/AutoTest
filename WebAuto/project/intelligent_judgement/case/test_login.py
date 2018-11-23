# -*- coding: utf-8 -*-
import unittest
from WebAuto.project.intelligent_judgement.page.login_page import LoginPage
from WebAuto.project.intelligent_judgement.page.warningstatistics_page import WarningStatisticsPage
from WebAuto.common.data_handle import project_case_data_path
from WebAuto.common.json_handle import JsonHandle
project="intelligent_judgement"
case_json_data=JsonHandle(project_case_data_path(project,"case_data.json")).jData
test_login_data = case_json_data["start_login"]

class Login(unittest.TestCase):

    def setUp(self):
        self.page = LoginPage().lanuch(project)
        self.version = self.page.project_info[0]["test_version"]
        self.accept_next_alert = True
        self.accept_next_alert = True
        self.verificationErrors = []

    def tearDown(self):
        self.page.close()
        self.assertEqual([], self.verificationErrors)
        self.page.quit()

    
    def test_error_user_login(self):
        '''
        验证登录功能-输入错误的用户名、非空密码
        '''

        print("-------------------------------------------------StartTest:【登录页面】 输入错误的用户名、非空密码，提示“用户名输入错误”------------------------------------")
        self.page.login(**test_login_data["test_error_user"])
        self.page.getscreen("login_user_error")
        try:
            self.assertTrue(self.page.userWrongPresent)
            print("验证ok-用户名输入有误\n")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        print("--------------------------------------------------EndTest:【登录页面】 输入错误的用户名、非空密码，提示“用户名输入错误”------------------------------------")

    def test_error_password_login(self):
        '''
        验证登录功能-输入正确用户名、错误密码
        '''
        print(
            "-------------------------------------------------StartTest:【登录页面】输入正确用户名、错误密码，提示“密码输入错误”------------------------------------")
        self.page.login(**test_login_data["test_error_password"])
        self.page.getscreen("login_password_error")
        try:
            self.assertTrue(self.page.passwordWrongPresent)
            print("验证ok-密码输入错误\n")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        print(
            "-------------------------------------------------EndTest:【登录页面】输入正确用户名、错误密码，提示“密码输入错误”------------------------------------")

    def test_null_user_login(self):
        '''
        验证登录功能-输入空的用户名、非空密码
        '''
        print(
            "-------------------------------------------------StartTest:【登录页面】输入空的用户名、非空密码，提示“请输入用户名”------------------------------------")
        self.page.login(**test_login_data["test_null_user"])
        self.page.getscreen("login_user_null")
        try:
            self.assertTrue(self.page.userWrongPresent)
            print("验证ok-账户输入有误\n")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        print(
            "-------------------------------------------------EndTest:【登录页面】输入空的用户名、非空密码，提示“请输入用户名”------------------------------------")

    def test_null_password_login(self):
        '''
            验证登录功能-输入非空用户名、空的密码
        '''
        print(
            "-------------------------------------------------StartTest:【登录页面】 输入非空用户名、空的密码，提示“请输入密码”------------------------------------")
        self.page.login(**test_login_data["test_null_password"])
        self.page.getscreen("login_password_null")
        try:
            self.assertTrue(self.page.passwordWrongPresent)
            print("验证ok-密码输入错误\n")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        print(
            "-------------------------------------------------EndTest:【登录页面】 输入非空用户名、空的密码，提示“请输入密码”------------------------------------")

    def test_correct_login(self):
        '''
           验证登录功能-输入正确的用户名和密码
        '''
        print(
            "-------------------------------------------------StartTest:【登录页面】输入正确的用户名和密码，成功登陆------------------------------------")
        self.page.login(**test_login_data["test_correct_login"])
        self.page.getscreen("login_success")
        self.page = WarningStatisticsPage(self.page)

        if self.version == "jsgy":
            try:
                self.assertEqual(u"综合预警统计分析", self.page.title())
            except AssertionError as e:
                self.verificationErrors.append(str(e))
            try:
                self.assertEqual(self.version, self.page.userName())
                print("验证ok-成功登陆\n")
            except AssertionError as e:
                self.verificationErrors.append("账号名显示有误：" + str(e))
                print("账号名显示有误："+str(e))
            self.page.getscreen("login_earlywarning")
        print(self.page.getCookies())
        print(
            "-------------------------------------------------EndTest:【登录页面】 输入正确的用户名和密码，成功登陆------------------------------------")


if __name__ == "__main__":
    unittest.main()
