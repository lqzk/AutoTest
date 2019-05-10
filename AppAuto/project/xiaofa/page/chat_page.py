from AppAuto.project.weixin.page.login_page import LoginPage



class ChatPage(LoginPage):
    wexin_button=("name","微信")
    address_book_button=("name","通讯录")
    find_button=("name","发现")
    self_button=("name","我")
    return_button = ("xpath", "//android.widget.ImageView[@content-desc=\"返回\"]")
    #备注解释contains用法：//*[contains(@text, '文字')]
    program_name = lambda self, name: ("xpath", "//*[contains(@text, '" + name + "')]")
    return_buttom_small_program = ("xpath", "//android.widget.FrameLayout[1]//android.widget.FrameLayout[2]/android.widget.ImageButton[1]")




    def check_chat_page(self):
        check_result=True
        elements=[self.wexin_button,self.address_book_button,self.find_button,self.self_button]
        for e in elements:
            check_result=check_result and self.is_display(*e)
        return check_result

    def jump_to_chat_page(self):
        self.click(*self.wexin_button)


    def jump_to_address_book_page(self):
        self.click(*self.address_book_button)

    def jump_to_find_page(self):
        self.click(*self.find_button)

    def jump_to_self_page(self):
        self.click(*self.self_button)

    def diect_to_small_program(self,name):
        self.swipe_down()
        self.click(*self.program_name(name))
        # self.click(*self.return_buttom_small_program)








    



