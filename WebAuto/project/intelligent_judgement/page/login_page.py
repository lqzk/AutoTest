from WebAuto.common.page import Page


class LoginPage(Page):


    __user_input=("id","user")
    __password_input=("id","password")
    __login_button=("css","div.login_btn > span")
    user_present=("xpath",".//*[@id='app']/div/div/div/div[2]/span")

    __user_wrong_present=("css","img.user_wrong")
    __password_wrong_present = ("css", "img.password_wrong")


    def login(self,user=None,password=None):
        account = self.project_info[1]
        if user==None:
            user = account["username"]
        if password==None:
            password = account["password"]

        print("登录用户:" + user + "，密码:" + password)
        self.clear(*self.__user_input)
        self.type(user,*self.__user_input)
        self.clear(*self.__password_input)
        self.type(password,*self.__password_input)
        self.click(*self.__login_button)
        self.sleep()


    def userWrongPresent(self):
        return self.is_element_present(*self.__user_wrong_present)

    def passwordWrongPresent(self):
        return self.is_element_present(*self.__password_wrong_present)











