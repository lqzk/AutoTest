from WebAuto.project.xiaofa.page.main_page import MainPage
import re

class PenaltyPage(MainPage):
    ensure_button=("xpath","//*[contains(text(),'免责声明')]/parent::*/parent::*//*[contains(text(),'确 定')]")
    forecast_button=("xpath","//*[contains(text(),'预测')]")

    def set_numerical_plot(self,numerical_plot_data):
        numerical_plot=lambda n:("xpath","//*[contains(text(),'"+n+"')]/parent::*//div/input")
        for k, v in numerical_plot_data.items():
            print("{0}:{1}".format(k, v))
            self.clear(*numerical_plot(k))
            self.type(v,*numerical_plot(k))

    def set_select_plot(self,select_plot_data):
        select_plot=lambda select:("xpath","//p[contains(text(),'*(必选项)')]/parent::*/p[contains(text(),'"+select+"')]/parent::*/parent::*//div[2]")
        for k, v in select_plot_data.items():
            print("{0}:{1}".format(k, v))
            self.sleep(0.5)
            self.click(*select_plot(k))
            self.sleep(1)
            two_select_plot=lambda select:("xpath","//*[contains(text(),'"+select+"')]")
            self.click(*two_select_plot(v))
            self.sleep(1)

    def set_click_plot(self,click_plot_data):
        click_plot=lambda n:("xpath","//*[contains(text(),'"+n+"')]")
        if not click_plot_data==[]:
            print("要素补充:{0}".format(click_plot_data))
            for each_v in click_plot_data:
                self.click(*click_plot(each_v))


    def set_penalty_data(self,data):
        print("确认免责声明")
        self.sleep(1)
        self.click(*self.ensure_button)
        print("设置情节")
        self.set_numerical_plot(data["numerical_plot"])
        self.set_select_plot(data["select_plot"])
        self.set_click_plot(data["click_plot"])
        print("点击预测按钮")
        self.click(*self.forecast_button)
        print("【page】跳转到量刑结果页面")


class PenaltyResultPage(PenaltyPage):
    criminal_publish_column= ("xpath", "//li[contains(text(),'量刑预测')]")
    similiar_case_column= ("xpath", "//li[contains(text(),'相似案例')]")
    similiar_law_column = ("xpath", "//li[contains(text(),'相关法条')]")
    criminal_guidance_column=("xpath", "//li[contains(text(),'量刑指导')]")

    def obtain_criminal_publish_result(self):
        self.sleep(1)
        self.click(*self.criminal_publish_column)

        predict_sentence = ("xpath", "//*[contains(text(),'预测刑期:')]/parent::*/p[2]")
        predict_sentence_content=self.text(*predict_sentence)
        print("预测刑期：{0}".format(predict_sentence_content))

        predict_fine = ("xpath", "//*[contains(text(),'预测罚金:')]/parent::*/p[2]")
        predict_fine_content = self.text(*predict_fine)
        print("预测罚金：{0}".format(predict_fine_content))

        predict_probation = ("xpath", "//*[contains(text(),'预测缓刑:')]/parent::*/div/p")
        predict_probation_content = self.text(*predict_probation)
        print("预测缓刑：{0}".format(predict_probation_content))

        criminal_publish_range = ("xpath", "//*[contains(text(),'量刑范围:')]/parent::*/p[2]")
        criminal_publish_range_content = self.text(*criminal_publish_range)
        print("量刑范围：{0}".format(criminal_publish_range_content))

        return predict_sentence_content,predict_fine_content,predict_probation_content,criminal_publish_range_content

    def obtain_similiar_case(self):
        self.click(*self.similiar_case_column)
        # case_list=("css", "div.penalty-result-page.scroll-div")
        # self.is_displayed(*case_list)
        case_list=("css", "div.el-card__body")
        try:
         self.find_elements(*case_list)
        except Exception:
            raise Exception("相似案例数据异常：找不到案例")


    def obtain_similiar_law(self):
        self.click(*self.similiar_law_column)
        # law_list=("css", "div.penalty-result-page.scroll-div")
        # self.is_displayed(*law_list)
        law_list=("css", "div.el-card__body")
        try:
         self.find_elements(*law_list)
        except Exception:
            raise Exception("相关法条数据异常：找不到法条")

    def obtain_criminal_guidance(self):
        self.click(*self.criminal_guidance_column)
        present_sentence=lambda s:("xpath", "//*[contains(text(),'"+s+"')]")
        start_sentence=self.text(*present_sentence("量刑起点:")).split(":")[1]
        base_santence=self.text(*present_sentence("基准刑:")).split(":")[1]
        declare_sentence=self.text(*present_sentence("宣告刑:")).split(":")[1]
        print("量刑起点:{0}\n基准刑:{1}\n宣告刑:{2}".format(start_sentence,base_santence,declare_sentence))
        return start_sentence,base_santence,declare_sentence

    def obtain_except_criminal_publish_result(self,data):
        ec_data=data["except_value"]
        ec_sentence=ec_data["预测刑期"]
        ec_fine=ec_data["预测罚金"]
        ec_probation=ec_data["预测缓刑"]
        ec_sentence_range=ec_data["量刑范围"]
        return ec_sentence,ec_fine,ec_probation,ec_sentence_range

    def extract_date(self,string):
        year, month, day = 0, 0, 0
        if re.search(u"(\d*)年", string): year = int(re.search(u"(\d*)年", string).group(1))
        if not year == 0:
            if re.search(u"年(\d*).*月", string): month = int(re.search(u"年(\d*).*月", string).group(1))
        else:
            if re.search(u"^(\d*).*月", string): month = int(re.search(u"^(\d*).*月", string).group(1))
        if re.search(u"(\d*)天", string): day = int(re.search(u"(\d*)天", string).group(1))
        return year, month, day

    def check_criminal_publish_result(self,data):
        sentence_content,fine_content,probation_content,sentence_range_content=self.obtain_criminal_publish_result()
        if data.get("except_value"):
            ec_sentence,ec_fine,ec_probation,ec_sentence_range=self.obtain_except_criminal_publish_result(data)
            if not sentence_range_content== ec_sentence_range:
                raise Exception("预测数据异常：与期望输出不一致（预测量刑范围：{0} ,实际量刑范围：{1}）".format(ec_sentence_range,sentence_range_content))

        if sentence_content=="--" and not probation_content =="--":
            raise Exception("缓刑数据异常：没有刑期，就不应该有缓刑")
        elif not sentence_content=="--" and not probation_content =="--":
            sentence_year, sentence_month, sentence_day = self.extract_date(sentence_content)
            sentence = sentence_year * 365 + sentence_month * 30 + sentence_day
            print(sentence)

            probation_year, probation_month, probation_day =self.extract_date(probation_content)
            probation = probation_year * 365 + probation_month * 30 + probation_day
            print(probation)

            if sentence>probation:
                raise Exception("数据异常：刑期不可大于缓刑")

        start_sentence, base_santence, declare_sentence=self.obtain_criminal_guidance()
        if not (self.extract_date(declare_sentence.split("～")[0]) == self.extract_date(
                sentence_range_content.split("~")[0]) and self.extract_date(
            declare_sentence.split("～")[1]) == self.extract_date(sentence_range_content.split("~")[1])):
            raise Exception("数据异常：量刑范围与宣告刑期不一致（{0} ！= {1}）".format(sentence_range_content, declare_sentence))

    def check_penaltyResult(self,data):
        self.check_criminal_publish_result(data)
        self.obtain_similiar_case()
        self.obtain_similiar_law()










