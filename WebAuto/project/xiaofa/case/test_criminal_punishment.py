import unittest
from WebAuto.common import ddt
from WebAuto.project.xiaofa.page.main_page import MainPage
from WebAuto.project.xiaofa.page.penalty_page import PenaltyPage,PenaltyResultPage
from WebAuto.common.data_handle import project_data
project_name="xiaofa"
project_info=project_data(project_name)
criminal_punlishment_data=project_info["criminal_punlishment"]
jiaotongzhaoshi_data=criminal_punlishment_data["交通肇事"]
guyihsanghai_data=criminal_punlishment_data["故意伤害"]
daoqie_data=criminal_punlishment_data["盗窃"]
weixianjiashi_data=criminal_punlishment_data["危险驾驶"]
qiaozhalesuo_data=criminal_punlishment_data["敲诈勒索"]
qiangjie_data=criminal_punlishment_data["抢劫"]
feifajujin_data=criminal_punlishment_data["非法拘禁"]
qiangduo_data=criminal_punlishment_data["抢夺"]


@ddt.ddt
class Criminal_Punlishment(unittest.TestCase):

    def setUp(self):
        self.page=MainPage().lanuch(project_info["test_driver"],project_info["url"])
        self.page.jumpto_module_criminal_publish()

    def tearDown(self):
        self.page.quit()

    @ddt.data(*jiaotongzhaoshi_data)
    def test_jiaotongzhaoshi(self,case_data):
        self.page.jumpto_page_penalty("51")
        self.page=PenaltyPage(self.page)
        self.page.set_penalty_data(case_data)
        self.page=PenaltyResultPage(self.page)
        self.page.check_penaltyResult(case_data)

    @ddt.data(*guyihsanghai_data)
    def test_guyihsanghai(self, case_data):
        self.page.jumpto_page_penalty("164")
        self.page = PenaltyPage(self.page)
        self.page.set_penalty_data(case_data)
        self.page = PenaltyResultPage(self.page)
        self.page.check_penaltyResult(case_data)

    @ddt.data(*daoqie_data)
    def test_daoqie(self, case_data):
        self.page.jumpto_page_penalty("201")
        self.page = PenaltyPage(self.page)
        self.page.set_penalty_data(case_data)
        self.page = PenaltyResultPage(self.page)
        self.page.check_penaltyResult(case_data)

    @ddt.data(*weixianjiashi_data)
    def test_weixianjiashi(self, case_data):
        self.page.jumpto_page_penalty("4169")
        self.page = PenaltyPage(self.page)
        self.page.set_penalty_data(case_data)
        self.page = PenaltyResultPage(self.page)
        self.page.check_penaltyResult(case_data)

    @ddt.data(*qiaozhalesuo_data)
    def test_qiaozahlesuo(self, case_data):
        self.page.jumpto_page_penalty("209")
        self.page = PenaltyPage(self.page)
        self.page.set_penalty_data(case_data)
        self.page = PenaltyResultPage(self.page)
        self.page.check_penaltyResult(case_data)

    @ddt.data(*qiangjie_data)
    def test_qiangjie(self, case_data):
        self.page.jumpto_page_penalty("200")
        self.page = PenaltyPage(self.page)
        self.page.set_penalty_data(case_data)
        self.page = PenaltyResultPage(self.page)
        self.page.check_penaltyResult(case_data)

    @ddt.data(*feifajujin_data)
    def test_feifajujin(self, case_data):
        self.page.jumpto_page_penalty("170")
        self.page = PenaltyPage(self.page)
        self.page.set_penalty_data(case_data)
        self.page = PenaltyResultPage(self.page)
        self.page.check_penaltyResult(case_data)

    @ddt.data(*qiangduo_data)
    def test_qiangduo(self, case_data):
        self.page.jumpto_page_penalty("203")
        self.page = PenaltyPage(self.page)
        self.page.set_penalty_data(case_data)
        self.page = PenaltyResultPage(self.page)
        self.page.check_penaltyResult(case_data)


if __name__ == '__main__':
    unittest.main()
