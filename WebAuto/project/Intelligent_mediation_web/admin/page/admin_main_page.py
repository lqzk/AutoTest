from WebAuto.project.Intelligent_mediation_web.admin.page.admin_login_page import AdminLoginPage

class AdminMainPage(AdminLoginPage):
    account=("css","span.username > span")
    allocate_institution_button=("xpath","//span[contains(text(), '分配机构')]")


    add_institution_button=("xpath","//button[contains(text(),'添加机构')]")
    institution_name_input=("xpath","//*[contains(@placeholder,'请输入机构名称')]")
    institution_account_input = ("xpath", "//*[contains(@placeholder,'请输入机构账号')]")
    institution_type_option = ("xpath", "//*[contains(@placeholder,'请选择机构类型')]")
    institution_field_option = ("css", "input.el-select__input")
    institution_leader_input = ("xpath", "//*[contains(@placeholder,'请输入机构负责人')]")
    institution_create_date_option = ("xpath", "//*[contains(@placeholder,'请选择机构成立日期')]")
    phone_input = ("xpath", "//*[contains(@placeholder,'请输入联系电话')]")
    institution_address1_option=("xpath", "//*[contains(@placeholder,'请选择省')]")
    institution_address2_option = ("xpath", "//*[contains(@placeholder,'请选择市')]")
    institution_address3_option = ("xpath", "//*[contains(@placeholder,'请选择区')]")
    institution_street_input=("xpath", "//*[contains(@placeholder,'请输入街道信息')]")
    institution_password_input=("xpath", "//*[contains(@placeholder,'请输入密码')]")
    institution_overdue_date_input=("xpath", "//*[contains(@placeholder,'选择日期')]")
    institution_ensure_button=("css",".yes")


    institution_list1_name_present=("xpath","//tbody/tr/td/div")
    institution_list1_account_present = ("xpath", "//tbody/tr/td[2]/div")



    def get_account_name(self):
        account_name=self.text(*self.account)
        print("登录账号为：{0}".format(account_name))
        return account_name

    def jump_to_institution_list(self):
        self.click(*self.allocate_institution_button)
        print("跳转到分配机构页面")

    def setInstitutionType(self,type):
        self.click(*self.institution_type_option)
        print("点击选择机构")
        chose_institution=("xpath","//span[contains(text(), '{0}')]".format(type))
        self.click(*chose_institution)
        print("选择机构：{0}".format(type))
        self.click(*self.institution_name_input)

    def setInstitutionField(self,field):
        self.click(*self.institution_field_option)
        print("点击选择擅长领域")
        chose_field=("xpath","//span[contains(text(), '{0}')]".format(field))
        self.click(*chose_field)
        print("选择擅长领域：{0}".format(field))
        self.click(*self.institution_name_input)

    def setInstitutionCreateDate(self,create_date):
        self.type(create_date,*self.institution_create_date_option)
        print("选择机构成立日期：{0}".format(create_date))
        self.click(*self.institution_name_input)

    def setInstitutionAddress(self,address1,address2,address3):
        chose_address1=("xpath","//span[contains(text(), '{0}')]".format(address1))
        chose_address2 = ("xpath", "//span[contains(text(), '{0}')]".format(address2))
        chose_address3 = ("xpath", "//span[contains(text(), '{0}')]".format(address3))
        self.click(*self.institution_address1_option)
        print("点击选择省份")
        self.click(*chose_address1)
        print("选择省份：{0}".format(address1))
        self.click(*self.institution_name_input)

        self.click(*self.institution_address2_option)
        print("点击选择市")
        self.click(*chose_address2)
        print("选择市：{0}".format(address2))
        self.click(*self.institution_name_input)

        self.click(*self.institution_address3_option)
        print("点击选择市辖区")
        self.click(*chose_address3)
        print("选择市辖区：{0}".format(address3))
        self.click(*self.institution_name_input)

    def setInstitutionOverdueDate(self,overdue_date):
        self.type(overdue_date,*self.institution_overdue_date_input)
        print("选择过期日期：{0}".format(overdue_date))
        self.click(*self.institution_name_input)

    def add_institution(self,name,account,type,field,leader,create_date,phone,address1,address2,address3,street,password,overdue_date):
        self.click(*self.add_institution_button)
        print("点击添加机构")

        self.type(name,*self.institution_name_input)
        print("输入机构名称：{0}".format(name))

        self.type(account, *self.institution_account_input)
        print("输入机构账户：{0}".format(account))

        self.setInstitutionType(type)
        self.setInstitutionField(field)

        self.type(leader, *self.institution_leader_input)
        print("输入机构负责人：{0}".format(leader))

        self.setInstitutionCreateDate(create_date)

        self.type(phone, *self.phone_input)
        print("输入联系电话：{0}".format(phone))

        self.setInstitutionAddress(address1,address2,address3)

        self.type(street, *self.institution_street_input)
        print("输入街道信息：{0}".format(street))

        self.type(password, *self.institution_password_input)
        print("输入密码：{0}".format(password))

        self.setInstitutionOverdueDate(overdue_date)

        self.click(*self.institution_ensure_button)
        print("点击确定按钮")


    def get_institutionlist1(self):
        institution_list1_name=self.text(*self.institution_list1_name_present)
        print("机构列表第一个机构的机构名称：{0}".format(institution_list1_name))
        institution_list1_account=self.text(*self.institution_list1_account_present)
        print("机构列表第一个机构的机构账号：{0}".format(institution_list1_account))
        return institution_list1_name,institution_list1_account













