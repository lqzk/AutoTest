from AppAuto.project.weixin.page.chat_page import ChatPage


class FindPage(ChatPage):
    small_program_button=("name","小程序")
    # program_name=lambda self,name:("xpath","//android.widget.TextView[@text=\'" + name + "\']")
    # program_name=lambda self,name:("xpath","//*[contains(@text, '" + name + "')]")


    def check_find_page(self):
        check_result=True
        elements=[self.small_program_button]
        for e in elements:
            check_result=check_result and self.is_display(*e)
        return check_result

    def enter_to_small_program(self,name):
        self.click(*self.small_program_button)
        print("进入小程序")
        self.click(*self.program_name(name))


