#-*- coding utf-8 -*-
import unittest

from WebAuto.project.intelligent_judgement.page.login_page import LoginPage
from WebAuto.project.intelligent_judgement.page.warningstatistics_page import WarningStatisticsPage
from WebAuto.project.intelligent_judgement.page.caselist_page import CaselistPage
from WebAuto.project.intelligent_judgement.page.casestudy_page import CaseStudyPage

from WebAuto.common.excel_data import Excel_Data
from WebAuto.project.intelligent_judgement.common import achive_filepath,cutout_content,read_file
from WebAuto.common.data_handle import project_data_path,project_case_data_path
project="intelligent_judgement"
project_data=lambda r:Excel_Data(project_data_path(project),r)




class Caselist(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.page = LoginPage().lanuch(project)
        cls.page.login()
        cls.version=cls.page.project_info[0]["test_version"]
        if cls.version == "jsgy":
            cls.page = WarningStatisticsPage(cls.page)
            cls.page.jump_warn_to_list()
        cls.page = CaselistPage(cls.page)

    @classmethod
    def tearDownClass(cls):
        pass



    def setUp(self):
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.assertEqual([],self.verificationErrors)


    def test_analysis_fromExcel(self):
        """
        研判分析功能测试--文书片段
        :return:
        """
        print('=================================================StartTest:【案件列表】研判分析_fromExcel====================================================')

        test_data=project_data("研判分析_短文本")
        data_list = test_data.data
        for data in data_list:
            try:
                data.update(self.test_analysis(data["测试文本"]))
            except Exception as e:
                raise Exception(e)
            finally:
                test_data.data = data

        print('=================================================EndTest:【案件列表】研判分析_fromExcel====================================================')



    def test_analysis_fromfile(self):
        """
        研判分析功能测试--文书全文
        """

        print('=================================================StartTest:【案件列表】研判分析_fromFile====================================================')

        test_data=project_data("研判分析_长文本")

        file_path=project_case_data_path(project,"长文本研判分析")
        dicfile = achive_filepath.achive_file(file_path)
        content_list=read_file.read(dicfile)
        for read_obj in content_list:
            content=read_obj[2]

            if "查明" in content:
                test_content = cutout_content.cutout_content(content, "查明部分")
            else:
                test_content = cutout_content.cutout_content(content, "指控部分")

            if test_content:
                data={}
                data["filename"]=read_obj[0]
                data["filepath"] =read_obj[1]

                try:
                    data.update(self.test_analysis(test_content,data["filename"]))
                except Exception as e:
                    raise Exception(e)
                finally:
                    test_data.data = data

        print('==================================================EndTest:【案件列表】研判分析_fromFile====================================================')


    def test_analysis(self,content=None,title=""):
        """
        研判分析功能测试--单次测试
        :param dicResult:
        :param dicResult_fail:
        :param param:
        :return:
        """
        print("----------------------------StartTest:【案件列表】研判分析_单次测试-----------------------------------")
        if content==None:
            content="盗窃500"

        dicResult= {}
        dicResult["测试文本"] = content
        analysis_state=self.page.predict_click(content)
        if analysis_state!="成功":
            dicResult["解析情况"]=analysis_state
        else:
            dicResult["解析情况"] = analysis_state
            try:
                self.page = CaseStudyPage(self.page)
                dicResult.update(self.page.info(self.version,title))
            except Exception as e:
                raise Exception(e)
            finally:
                self.page.jump_study_to_list()
        print("-----------------------------EndTest:【案件列表】研判分析_单次测试---------------------------------------")
        return dicResult


    def test_upload(self):
        upload_file_dir=project_case_data_path(project,"文书上传")
        files = achive_filepath.achive_file(upload_file_dir)
        for filename, filepath in files.items():
            case_no = self.page.upload_file(filepath)
            self.assertNotEqual(case_no,None)



if __name__ == "__main__":
    unittest.main()
