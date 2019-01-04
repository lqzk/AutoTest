# -*- coding: utf-8 -*-
import unittest
from WebAuto.project.Intelligent_mediation_web.admin.page.admin_login_page import AdminLoginPage
from WebAuto.project.Intelligent_mediation_web.admin.page.admin_main_page import AdminMainPage
from WebAuto.common.data_handle import project_data,project_info
project="Intelligent_mediation_web"
all_project_data=project_data(project)
browser_type=project_info(all_project_data,"test_driver")
url=project_info(all_project_data,"AdminURL")

class AdminLogin(unittest.TestCase):

    def setUp(self):
        self.page = AdminLoginPage().lanuch(browser_type, url)

    def tearDown(self):
        self.page.close()
        self.page.quit()

    def test_supper_login(self):
        '''验证登录超级管理员账户'''
        try:
            test_account = project_info(all_project_data, "SupperUser.Login")
            self.page.login(*test_account.values())
            self.assertEqual(test_account["Username"], AdminMainPage(self.page).get_account_name())
            print("【验证成功】成功登录超级管理员账号")
        except Exception as e:
            print("【验证失败】登录超级管理员账号失败，error_info:{0}".format(e))



if __name__ == "__main__":
    unittest.main()
