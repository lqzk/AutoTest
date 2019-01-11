import unittest
from InterfaceAuto.common import ddt
from InterfaceAuto.common.data_handle import DataHandle
from InterfaceAuto.common.general_test import GeneralTest
project = "Risk_assess"
sun_project="Risk_assess_foreground"
module = "docdispose"
module_cases=DataHandle().obtain_interface_cases(project, module,sun_project=sun_project)
table_result=[]

@ddt.ddt
class TestCase(unittest.TestCase):

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
