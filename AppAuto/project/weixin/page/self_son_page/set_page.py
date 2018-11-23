from AppAuto.project.weixin.page.self_page import SelfPage

class SetPage(SelfPage):
    logout_button=("name","退出")
    close_wexin_button=("name","关闭微信")
    logout_log_button=("name","退出登录")
    confirm_logout_button=("name","退出")
    confirm_cancel_button=("name","取消")

    def check_set_page(self):
        check_result=True
        elements=[self.logout_button]
        for e in elements:
            check_result=check_result and self.is_display(*e)
        return check_result



    def logout(self,logout_log=True,close_wexin=False):
        self.click(*self.logout_button)

        if logout_log:
            self.click(*self.logout_log_button)
            self.click(*self.confirm_logout_button)
        elif close_wexin:
            self.click(*self.close_wexin_button)
            self.click(*self.confirm_logout_button)
        else:
            self.tap(500,400,500)







