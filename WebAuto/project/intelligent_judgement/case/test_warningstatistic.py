#-*- coding utf-8 -*-
import unittest
from WebAuto.project.intelligent_judgement.page.login_page import LoginPage
from WebAuto.project.intelligent_judgement.page.warningstatistics_page import WarningStatisticsPage
from WebAuto.project.intelligent_judgement.page.caselist_page import CaselistPage
from WebAuto.common.data_handle import project_case_data_path,DataHandle
from WebAuto.common.json_handle import JsonHandle
project="intelligent_judgement"
case_json_data=JsonHandle(project_case_data_path(project,"case_data.json")).jData
version= DataHandle().obtain_project_info(project)[0]["test_version"]


@unittest.skipIf(version!="jsgy","version")
class WarningStatistic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.page = LoginPage().lanuch(project)
        cls.page.login()
        cls.page = WarningStatisticsPage(cls.page)
        cls.accept_next_alert = True

    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        self.verificationErrors = []

    def tearDown(self):
        # self.page.close()
        self.assertEqual([], self.verificationErrors)


    def test_timefliter(self):
        """
        验证偏离度预警案件分布-时间筛选
        """
        time_datas=case_json_data["common"]["timefliter"]

        for tdata in time_datas:
            dictdata=DataHandle().timeData_handle(**tdata)
            self.page.time_filter(**dictdata)

    def test_warning_aggreement(self):
        """
        验证预警页面偏离度里外一致
        :return: 返回测试结果
        """

        print("----------------------验证预警页面偏离度里外一致,次数3-----------------------")
        count=0
        for count in range(3):
            print("----------------------subTest：验证预警页面偏离度里外一致之第{}次验证-----------------------".format(count+1))
            for level in range(3):
                print("验证预警页面偏离度里外一致之{0}级预警".format(level+1))
                warning_num=self.page.warning_present()
                jump_result=self.page.warning_jump(level + 1)
                if jump_result==False:
                    continue
                else:
                    level_num=warning_num[level]
                    self.page=CaselistPage(self.page)
                    if self.page.total_count_present()==level_num:
                        self.page.jump_list_to_warn()
                        if self.page.warning_present()==warning_num:
                            print("验证预警页面偏离度里外一致之{0}级预警，成功".format(level+1))
                        else:
                            print("验证失败:外外不一致")
                            self.verificationErrors.append("验证失败:外外不一致")
                            return False
                    else:
                        print("验证失败:里外不一致")
                        self.verificationErrors.append("验证失败:里外不一致")
                        return False
            print("----------------------验证预警页面偏离度里外一致之第{}次验证,成功-----------------------".format(count+1))
        if count>=2:
            print("----------------------结果：验证预警页面偏离度里外一致,成功-----------------------")
            return True


    def test_casecausefliter(self):
        """
        验证预警案件数量趋势图-案由筛选
        :return:
        """
        case_datas=case_json_data["common"]["casefliter"]["case_cause_test"]
        print('=====StartTest:预警案件数量趋势图-案由筛选,测试案由{0}======'.format(case_datas))

        for casecause in case_datas:
            self.page.casecausefliter(casecause)
        print('=====EndTest:预警案件数量趋势图-案由筛选======')



if __name__ == "__main__":
    unittest.main()
