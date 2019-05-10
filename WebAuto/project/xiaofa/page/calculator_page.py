from WebAuto.project.xiaofa.page.main_page import MainPage
import re

class CalculatorPage(MainPage):
    calculator_button=("xpath","//*[contains(text(),'计算结果')]")
    ensure_button = ("xpath", "//*[contains(text(),'免责声明')]/parent::*/parent::*//*[contains(text(),'确 定')]")
    answer = ("css", "div.answer")

    def set_numerical_condition(self,numerical_condition_data):
        numerical_condition=lambda n:("xpath","//*[contains(text(),'"+n+"')]/parent::*//div/input")
        for k, v in numerical_condition_data.items():
            print("{0}:{1}".format(k, v))
            self.type(v,*numerical_condition(k))

    def set_select_condition(self,select_condition_data):
        select_condition=lambda select:("xpath","//label[contains(text(),'"+select+"')]/parent::*/div/div/div/input")
        for k, v in select_condition_data.items():
            print("{0}:{1}".format(k, v))
            self.sleep(0.5)
            self.click(*select_condition(k))
            self.sleep(0.5)
            two_select_condition=lambda select:("xpath","//span[contains(text(),'"+select+"')]")
            self.find_element(*two_select_condition(v))
            self.click(*two_select_condition(v))



    def set_calculator_data(self,data):
        print("确认免责声明")
        self.sleep(1)
        self.click(*self.ensure_button)
        print("设置情节")
        self.set_select_condition(data["select_condition"])
        self.set_numerical_condition(data["numerical_condition"])
        print("点击计算按钮")
        self.click(*self.calculator_button)
        self.sleep(1)

    def check_calculator_result(self,type,data):
        self.set_calculator_data(data)
        if type=="legal":
            result = float(self.text(*self.answer).split("元")[0])
            print("【诉讼费用】计算结果：{0}元".format(result))
            if result<0:
                raise Exception("【诉讼费用】计算结果错误：为负数")

        elif type=="injury":
            result = []
            results_ele = self.find_elements(*self.answer)
            for each_answer_ele in results_ele:
                result.append(float(each_answer_ele.text.split("元")[0]))
            print(result)
            print("【工伤赔偿】计算结果：赔偿费用 {0}元，伤残津贴 {1}元".format(result[0], result[1]))
            if result[0]<0 or result[1]<0:
                raise Exception("【工伤赔偿】计算结果错误：为负数")

        elif type == "traffic":
            result =  float(self.text(*self.answer).split("元")[0])
            print("【交通赔偿】计算结果：{0}元".format(result))
            if result<0:
                raise Exception("【交通赔偿】计算结果错误：为负数")

        elif type == "lawyer":
            result = self.text(*self.answer).split("元")[0].split("-")
            result[0],result[1]=float(result[0]),float(result[1])
            print("【律师费用】计算结果：{0}-{1}元".format(result[0], result[1]))
            if result[0] < 0 or result[1] < 0:
                raise Exception("【律师费用】计算结果错误：为负数")
            elif result[0]>=result[1]:
                raise Exception("【律师费用】计算结果错误：范围错误")












