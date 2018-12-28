import unittest
from InterfaceAuto.common import ddt
from InterfaceAuto.common.data_handle import DataHandle
from InterfaceAuto.common.general_test import GeneralTest

project = "Intelligent_mediation"
module = "committee"
module_cases=DataHandle().obtain_interface_cases(project, module)
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
