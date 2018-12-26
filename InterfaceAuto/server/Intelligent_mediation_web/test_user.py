import unittest
from InterfaceAuto.common import ddt
from InterfaceAuto.common.data_handle import DataHandle,project_case_data
from InterfaceAuto.common.general_test import GeneralTest
project = "Intelligent_mediation_web"
module = "user"
module_cases=DataHandle().obtain_interface_cases(project, module)
case_result=project_case_data("{0}_result".format(project),module)
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
        try:
            self.run.execute_case(table_result)
        except Exception as e:
            raise Exception(e)
        finally:
            table_result[-1] = case_data
            case_result.data = case_data



if __name__ == '__main__':
    unittest.main()
