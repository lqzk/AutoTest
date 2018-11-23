import unittest
import warnings
from AppAuto.project.weixin.page.chat_page import ChatPage

project="weixin"

class TestChatPage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.page=ChatPage().launch(project)



    def test_1_this_page(self):
        self.page.jump_to_chat_page()
        self.assertTrue(self.page.check_chat_page())
        print("[page]进入微信聊天主页面")

    def test_direct_to_small_program(self):
        self.page.diect_to_small_program("ofo小黄车")



if __name__ == '__main__':
    suite=unittest.TestSuite()
    test_cases = [ TestChatPage('test_is_chat_book_page'),TestChatPage('test_direct_to_small_program')]
    suite.addTests(test_cases)
    runner=unittest.TextTestRunner()
    runner.run(test=suite)


