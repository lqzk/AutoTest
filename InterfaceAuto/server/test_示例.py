import unittest
from InterfaceAuto.common import ddt
from InterfaceAuto.common.data_handle import DataHandle,project_case_data
from InterfaceAuto.common.general_test import GeneralTest
project = "Intelligent_mediation"
module = "示例"
module_cases=DataHandle().obtain_interface_cases(project, table_name=module)
# module_cases=DataHandle().obtain_interface_cases(project, module)
case_result=project_case_data(project,"{0}_result".format(project),module)
table_result=[]

@ddt.ddt
class TestCase(unittest.TestCase):

    def setUp(self):
        self.run=GeneralTest()


    def tearDown(self):
        pass

    #类型一、excel记录结果
    @ddt.data(*module_cases)
    def test_module_cases(self,case_data):
        table_result.append(case_data)
        try:
            self.run.execute_case(table_result)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data = table_result[-1]

    #类型二、极简版
    @ddt.data(*module_cases)
    def test_module_cases(self,case_data):
        table_result.append(case_data)
        self.run.execute_case(table_result)



if __name__ == '__main__':
    unittest.main()
