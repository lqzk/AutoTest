import unittest
import ddt
from InterfaceAuto.common.data_handle import DataHandle,project_case_data
from InterfaceAuto.common.general_test import GeneralTest

project = "Intelligent_mediation"
module = "common"
cases=lambda interface: DataHandle().obtain_interface_cases(project, module, interface)
case_result=project_case_data(project,module)



@ddt.ddt
class TestCase(unittest.TestCase):

    def setUp(self):
        self.run=GeneralTest()

    def tearDown(self):
        pass

    @ddt.data(*cases("idcard_upload"))
    def test_idcard_upload(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


   

if __name__ == '__main__':
    unittest.main()
