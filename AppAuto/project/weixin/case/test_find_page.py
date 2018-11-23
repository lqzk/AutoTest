import unittest
import warnings
from AppAuto.project.weixin.page.find_page import FindPage

project="weixin"

class TestFindPage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.page=FindPage().launch(project)

    def test_1_this_page(self):
        self.page.jump_to_find_page()
        self.assertTrue(self.page.check_find_page())
        print("[page]进入发现主页面")

    def test_enter_small_program(self):
        self.page.enter_to_small_program("ofo小黄车官方版")

        self.page.sleep(10)

        print("缩小准备")
        self.page.smaller()
        print("缩小完成")
        self.page.sleep(10)

        print("放大准备")
        self.page.larger()
        print("放大完成")
        self.page.sleep(10)





if __name__ == '__main__':
    suite=unittest.TestSuite()
    test_cases = [ TestFindPage('test_is_find_page'),TestFindPage('test_enter_small_program')]
    suite.addTests(test_cases)
    runner=unittest.TextTestRunner()
    runner.run(test=suite)


