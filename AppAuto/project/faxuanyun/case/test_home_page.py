import unittest
import warnings

from AppAuto.project.faxuanyun.page.home_page import HomePage
from AppAuto.project.weixin.page.chat_page import ChatPage
project="faxuanyun"

class TestHomePage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        warnings.simplefilter("ignore",ResourceWarning)
        self.page=ChatPage().launch(project)
        self.page.sleep(2)
        self.page.diect_to_small_program("We打卡")
        self.page = HomePage(self.page)


    def test_is_home_page(self):
        self.assertTrue(self.page.check_home_page())

    def test_title(self):
        self.assertEqual(self.page.get_title(),"法宣云")



if __name__ == '__main__':
    suite=unittest.TestSuite()
    test_cases = [ TestHomePage('test_is_home_page'), TestHomePage('test_title')]
    suite.addTests(test_cases)
    runner=unittest.TextTestRunner(verbosity=2)
    runner.run(test=suite)

