# -*- coding: utf-8 -*-
import unittest
from WebAuto.project.Intelligent_mediation_web.admin.page.admin_login_page import AdminLoginPage
from WebAuto.project.Intelligent_mediation_web.admin.page.admin_main_page import AdminMainPage
from WebAuto.common.data_handle import project_data,project_info
project="Intelligent_mediation_web"
all_project_data=project_data(project)
browser_type=project_info(all_project_data,"test_driver")
url=project_info(all_project_data,"AdminURL")

class AdminInstitution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = AdminLoginPage().lanuch(browser_type, url)
        test_account = project_info(all_project_data, "SupperUser.Login")
        cls.page.login(*test_account.values())
        cls.page= AdminMainPage(cls.page)

    @classmethod
    def tearDownClass(cls):
        pass


    def setUp(self):
        pass

    def tearDown(self):
        self.page.close()
        self.page.quit()

    def test_1_Register(self):
        '''验证超级管理员添加机构'''
        try:
            print("\n【验证开始】超级管理员成功添加机构")
            self.page.jump_to_institution_list()
            self.page=AdminMainPage(self.page)
            register_info=project_info(all_project_data, "SupperUser.Register1")
            self.page.add_institution(*register_info.values())
            self.page.sleep(15)
            register_name,register_account=register_info["InstitutionName"],register_info["Username"]
            add_register_name,add_register_account=self.page.get_institutionlist1()
            self.assertEqual(register_name, add_register_name)
            self.assertEqual(register_account,add_register_account)
            print("【验证成功】超级管理员成功添加机构\n")
        except Exception as e:
            print("【验证失败】超级管理员添加机构失败，error_info:{0}\n".format(e))
            raise Exception("【验证失败】超级管理员添加机构失败，error_info:{0}\n".format(e))



if __name__ == "__main__":
    unittest.main()
