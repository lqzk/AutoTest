import unittest
import warnings
from AppAuto.project.weixin.page.self_page import SelfPage
from AppAuto.project.weixin.page.self_son_page.set_page import SetPage

project="weixin"

class TestSelfPage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.page=SelfPage().launch(project)
        self.page.jump_to_self_page()

    def test_1_this_page(self):
        self.assertTrue(self.page.check_self_page())
        print("[page]进入我主页面")



    def test_login_out(self):
        self.page.jump_to_set_page()
        self.page = SetPage(self.page)
        self.assertTrue(self.page.check_set_page())
        print("[page]进入我-设置页面")
        self.page = SetPage(self.page)
        self.page.swipe_up()
        self.page.logout()
        self.assertTrue(self.page.check_login_page())
        print("[logout]成功退出登录")



if __name__ == '__main__':
    suite=unittest.TestSuite()
    test_cases = [ TestSelfPage('test_is_self_page'),TestSelfPage('test_login_out')]
    suite.addTests(test_cases)
    runner=unittest.TextTestRunner()
    runner.run(test=suite)


