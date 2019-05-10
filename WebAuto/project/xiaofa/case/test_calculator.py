import unittest
from WebAuto.common import ddt
from WebAuto.project.xiaofa.page.main_page import MainPage
from WebAuto.project.xiaofa.page.calculator_page import CalculatorPage
from WebAuto.common.data_handle import project_data
project_name="xiaofa"
project_info=project_data(project_name)
calculator_data=project_info["calculator"]
susong_cost_data=calculator_data["诉讼费用"]
gonghsang_peichang_data=calculator_data["工伤赔偿"]
jiaotong_peichang_data=calculator_data["交通赔偿"]
lvshi_cost_data=calculator_data["律师费用"]

@ddt.ddt
class Calculator(unittest.TestCase):

    def setUp(self):
        self.page=MainPage().lanuch(project_info["test_driver"],project_info["url"])
        self.page.jumpto_module_calculator()

    def tearDown(self):
        self.page.quit()

    @ddt.data(*susong_cost_data)
    def test_susong_cost(self,case_data):
        type="legal"
        self.page.jumpto_page_calculate(type)
        self.page=CalculatorPage(self.page)
        self.page.check_calculator_result(type,case_data)

    @ddt.data(*gonghsang_peichang_data)
    def test_gonghsang_peichang(self,case_data):
        type="injury"
        self.page.jumpto_page_calculate(type)
        self.page=CalculatorPage(self.page)
        self.page.check_calculator_result(type,case_data)

    @ddt.data(*jiaotong_peichang_data)
    def test_jiaotong_peichang(self,case_data):
        type="traffic"
        self.page.jumpto_page_calculate(type)
        self.page=CalculatorPage(self.page)
        self.page.check_calculator_result(type,case_data)

    @ddt.data(*lvshi_cost_data)
    def test_lvshi_cost(self,case_data):
        type="lawyer"
        self.page.jumpto_page_calculate(type)
        self.page=CalculatorPage(self.page)
        self.page.check_calculator_result(type,case_data)


if __name__ == '__main__':
    unittest.main()
