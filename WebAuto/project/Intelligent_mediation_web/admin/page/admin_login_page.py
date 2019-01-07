from WebAuto.common.page import Page


class AdminLoginPage(Page):

    user_input=("xpath","//input[@type='text']")
    password_input=("xpath","//input[@type='password']")
    login_button=("css","div.submit")
    user_mediator_button=("css","span.el-radio__label")
    user_institution_button = ("css", ".el-radio:nth-child(2) > .el-radio__label")
    user_super_button = ("css", ".el-radio:nth-child(3) > .el-radio__label")

    def login(self,user,password,user_type):
        print("输入用户名：{0}".format(user))
        self.type(user,*self.user_input)
        print("输入密码：{0}".format(password))
        self.type(password,*self.password_input)
        if user_type==1:
            print("点击选择登录类别：调解员")
            self.click(*self.user_mediator_button)
        elif user_type==2:
            print("点击选择登录类别：机构管理员")
            self.click(*self.user_institution_button)
        elif user_type == 3:
            print("点击选择登录类别：超级管理员")
            self.click(*self.user_super_button)
        else:
            raise Exception("不存在的登录类别：{0}".format(user_type))
        self.click(*self.login_button)
        print("点击登录按钮")















