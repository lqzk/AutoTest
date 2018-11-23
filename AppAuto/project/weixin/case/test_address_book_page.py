import unittest
import warnings

from AppAuto.project.weixin.page.address_book_page import AddressBookPage

project="weixin"

class TestAddressBookPage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.page=AddressBookPage().launch(project)
        self.page.sleep(3)



    def test_1_this_page(self):
        self.page.jump_to_address_book_page()
        print("[page]进入通讯录主页面")
        self.assertTrue(self.page.check_address_book_page())


    def test_set_remarks_and_label(self):
        result=self.page.set_remarks_and_label("阿爸")
        self.assertTrue(result)
        print("[通讯录]成功出现备忘录和标签设置")
        self.page.tap()
        print("[通讯录]轻点某处，备忘录和标签设置消失")


    def test_group_chat(self):
        self.page.create_group_chat(["阿爸","阿妈"])
        print("[通讯录]进入群聊，选中创建成员，再返回")





if __name__ == '__main__':
    suite=unittest.TestSuite()
    test_cases = [ TestAddressBookPage('test_is_address_book_page'),TestAddressBookPage('test_set_remarks_and_label'),TestAddressBookPage('test_group_chat')]

    suite.addTests(test_cases)
    runner=unittest.TextTestRunner()
    runner.run(test=suite)


