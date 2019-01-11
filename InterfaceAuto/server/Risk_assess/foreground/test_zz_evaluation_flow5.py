import unittest
from InterfaceAuto.common import ddt
from InterfaceAuto.common.data_handle import DataHandle
from InterfaceAuto.common.general_test import GeneralTest
from InterfaceAuto.common.json_handle import JmespathExtractor
import json
JExtractor = JmespathExtractor()
project = "Risk_assess"
sun_project="Risk_assess_foreground"
module = "诉讼离婚纠纷2"
module_cases=DataHandle().obtain_interface_cases(project, table_name=module,sun_project=sun_project)
table_result=[]

@ddt.ddt
class TestCase(unittest.TestCase):
    '''【诉讼离婚纠纷2】数据关联，只需查看第一个错误接口'''

    def setUp(self):
        self.run=GeneralTest()

    def tearDown(self):
        pass

    @ddt.data(*module_cases)
    def test_module_cases(self,case_data):
        table_result.append(case_data)
        self.run.execute_case(table_result)








if __name__ == '__main__':
    unittest.main()
