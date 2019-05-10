from WebAuto.common.page import Page

class MainPage(Page):
    criminal_publish_button=("xpath","//button[contains(text(),'刑事量刑')]")
    calculator_button=("xpath","//button[contains(text(),'费用计算')]")

    def jumpto_module_criminal_publish(self):
        print("【page】当前为首页")
        print("跳到量刑预测模块")
        self.click(*self.criminal_publish_button)
        criminal_publish_title = ("xpath", "//*[contains(text(),'刑事量刑预测')]")
        self.is_displayed(*criminal_publish_title)

    def jumpto_module_calculator(self):
        print("【page】当前为首页")
        print("跳到费用计算器模块")
        self.click(*self.calculator_button)
        calculator_title = ("xpath", "//*[contains(text(),'费用计算')]")
        self.is_displayed(*calculator_title)

    def jumpto_page_penalty(self,id):
        self.sleep(1)
        print("【page】跳到量刑页面")
        penalty_button = lambda id: ("xpath", "//*[contains(@data-causeid,'" + id + "')]")
        self.click(*penalty_button(id))

    def jumpto_page_calculate(self,type):
        self.sleep(1)
        print("【page】跳到费用计算页面")
        penalty_button = lambda type: ("xpath", "//*[contains(@data-calcuid,'" + type + "')]")
        self.click(*penalty_button(type))





