from AppAuto.project.weixin.page.chat_page import ChatPage


class SelfPage(ChatPage):
    set_button=("name","设置")

    def check_self_page(self):
        check_result=True
        elements=[self.set_button]
        for e in elements:
            check_result=check_result and self.is_display(*e)
        return check_result


    def jump_to_set_page(self):
        self.click(*self.set_button)


