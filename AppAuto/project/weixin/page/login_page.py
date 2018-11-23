from AppAuto.common.page import Page

class LoginPage(Page):
    account=("xpath","//android.widget.TextView[@text=\'密码\']/parent::*/parent::*//android.widget.TextView[1]")
    password=("xpath","//android.widget.TextView[@text=\'密码\']/parent::*//android.widget.EditText[1]")
    login_button=("name","登录")

    def check_login_page(self):
        check_result=True
        elements=[self.login_button]
        for e in elements:
            check_result=check_result and self.is_display(*e)
        return check_result


    def get_account(self,):
        return  self.text(*self.account)


    def login_by_password(self,input_password):
        if self.is_enabled(*self.password):
            print("[login]input password：{0}".format(input_password))
            self.input(*self.password, input_value=input_password)
            if self.is_enabled(*self.login_button):
                print("[login]click login button")
                self.click(*self.login_button)
            else:
                print("[login]无法点击登录按钮，请确认是否可用")
        else:
            print("[login]无法输入密码，请重新尝试或者检查所在页面是否正确")









        