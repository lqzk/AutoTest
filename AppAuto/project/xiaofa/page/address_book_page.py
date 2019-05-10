from AppAuto.project.weixin.page.chat_page import ChatPage


class AddressBookPage(ChatPage):
    group_chat=("name","群聊")
    label=("name","标签")
    public_number=("name","公众号")
    set_remarks_and_label_button=("name","设置备注及标签")
    create_group_chat_button=("xpath","//android.widget.ImageButton[@content-desc=\"新群聊\"]")
    start_group_chat=("name","发起群聊")
    member_checkbox=lambda self,W:("xpath","//android.widget.TextView[@text=\'" + W + "\']/parent::*/parent::*/parent::*/android.widget.CheckBox")
    selected_member_img=lambda self,W:("xpath","//android.widget.ImageView[@content-desc=\'"+W+"\']")



    def check_address_book_page(self):
        check_result=True
        elements=[self.group_chat,self.label,self.public_number]
        for e in elements:
            check_result=check_result and self.is_display(*e)
        return check_result

    def set_remarks_and_label(self,target_name,set_remarks_value=None,set_label_value=None):
        self.long_press(*("name",target_name),long_duration=1000)
        if self.is_display(*self.set_remarks_and_label_button):
            return True
        else:
            return False

    def create_group_chat(self,group_list):
        self.click(*self.group_chat)
        self.click(*self.create_group_chat_button)
        is_checked=True
        if self.is_display(*self.start_group_chat):
            for member in group_list:
                self.click(*self.member_checkbox(member))
                is_checked=self.is_display(*self.selected_member_img(member)) and is_checked
                if is_checked==False:
                    print("{0}未显示选中图标".format(member))
        self.click(*self.return_button)
        self.click(*self.return_button)



























    



