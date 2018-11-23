from WebAuto.project.intelligent_judgement.page.warningstatistics_page import WarningStatisticsPage
import time

class CaselistPage(WarningStatisticsPage):
    __total_count = ("css", "div.total > span")
    __return_button = ("css", "div.to_count")

    predict_button=("css","div.predict_punish")
    predict_put=("id","case_input")
    predict_confirm=("css","div.confirm")
    predict_return=("css","div.return")
    analysis_warn_frame=("css","div.upload_warn_content")
    analysis_warn_content=("xpath","//div[@class='upload_warn_content']/p/span")
    page_tags=("css","ul.ant-pagination>li")

    upload_button=("css","div.upload_btn")
    file_put=("css","input[type=\'file\']")
    case_no=("xpath","//div[@id='app']/div/div[4]/div/div/div[3]/div/div[2]/span/span[2]")
    upload_error=("css",".check_content>div>p")
    skip_button=("css","#check_btn>div")



    def paging(self,tag_name):
        pages=self.find_elements(*self.page_tags)
        for page in pages:
            if page.get==tag_name:
                page.click()



    def total_count_present(self):
        self.sleep(4)
        total_num=self.text(*self.__total_count)
        print("案件列表页案件总数：{0}".format(total_num))
        return total_num

    def jump_list_to_warn(self):
        self.click(*self.__return_button)
        self.sleep()
        print('案件列表页面跳转预警统计页面')


    def predict_click(self,content):
        print("测试文本:{0}".format(content))
        analysis_result="成功"
        self.click(*self.predict_button)
        self.sleep(0.01)
        self.clear(*self.predict_put)
        self.sleep(0.01)
        self.click(*self.predict_put)
        self.type(content,*self.predict_put)
        self.click(*self.predict_confirm)


        if self.is_element_exsit(*self.analysis_warn_frame):
            analysis_result=self.text(*self.analysis_warn_content)
            print("研判分析失败：" + "\n 错误信息：" + analysis_result)
            self.click(*self.predict_return)
        return analysis_result



    def upload_file(self,file):
        # 文书上传
        self.click(*self.upload_button)
        with open(file):
            self.type(file, *self.file_put)
        try:
            self.find_element(*self.upload_error)
            error_info = self.text(*self.upload_error)
            print(error_info)
            # self.click(*self.skip_button)
            self.click(*self.predict_return)
        except:
            pass
        try:
            case = self.text(*self.case_no)
        except:
            case=None
        print("上传文书案号：{0}".format(case))
        return case

