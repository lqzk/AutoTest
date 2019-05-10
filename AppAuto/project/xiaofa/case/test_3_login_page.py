import unittest
import warnings
from AppAuto.project.weixin.page.chat_page import ChatPage
from AppAuto.project.weixin.page.login_page import LoginPage
from AppAuto.common.data_handle import DataHandle


project="xiaofa"

class TestLoginPage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.page=LoginPage().launch(project)

    def test_1_this_page(self):
        self.assertTrue(self.page.check_login_page())

    def test_2_login_by_password(self):
        login_account=DataHandle().obtain_login_account(project)
        login_account_name=login_account["account"]
        login_account_password=login_account["password"]
        current_account_name=self.page.get_account().replace(" ","")
        if login_account_name==current_account_name:
            self.page.login_by_password(login_account_password)
            print("[page]切换微信聊天主页面")
            self.page = ChatPage(self.page)
            self.assertTrue(self.page.check_chat_page())
            print("[login]登录成功,进入微信聊天主页面")
        else:
            print("[login]登录账户错误，当前账户为{0}，应为{1}".format(current_account_name,login_account_name))




if __name__ == '__main__':
    suite=unittest.TestSuite()
    test_cases = [ TestLoginPage('test_is_login_page'), TestLoginPage('test_login_by_password')]
    suite.addTests(test_cases)
    runner=unittest.TextTestRunner(verbosity=2)
    runner.run(test=suite)


