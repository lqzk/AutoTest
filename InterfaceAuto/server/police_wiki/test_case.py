import unittest
import ddt
from InterfaceAuto.common.data_handle import DataHandle,project_case_data
from InterfaceAuto.common.general_test import GeneralTest

project = "police_wiki"
module = "case"
cases=lambda interface: DataHandle().obtain_interface_cases(project, module, interface)
case_result=project_case_data(project,module)



@ddt.ddt
class TestCase(unittest.TestCase):

    def setUp(self):
        self.run=GeneralTest()

    def tearDown(self):
        pass

    @ddt.data(*cases("causeRecommend"))
    def test_case_recommmend(self,case_data):
        # print(case_data)
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


    @ddt.data(*cases("typicalList"))
    def test_typical_list(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


    @ddt.data(*cases("typicalDetail"))
    def test_typical_detail(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


if __name__ == '__main__':
    unittest.main()
