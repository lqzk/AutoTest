from WebAuto.project.Intelligent_mediation_web.admin.page.admin_login_page import AdminLoginPage

class AdminMainPage(AdminLoginPage):
    account=("css","span.username > span")

    allocate_institution_button=("xpath","//*[contains(@id,'children2')]/span[contains(text(), '分配机构')]")

    def get_account_name(self):
        account_name=self.text(*self.account)
        print("登录账号为：{0}".format(account_name))
        return account_name

    def jump_to_institution_list(self):
        print()
        self.click(*self.allocate_institution_button)
