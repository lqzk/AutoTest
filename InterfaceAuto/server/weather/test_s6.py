import unittest
import ddt
from InterfaceAuto.common.data_handle import DataHandle,project_case_data
from InterfaceAuto.common.general_test import GeneralTest
project = "weather"
module = "s6"
cases=lambda interface: DataHandle().obtain_interface_cases(project, module, interface)
case_result=project_case_data(project,module)

@ddt.ddt
class TestCase(unittest.TestCase):

    def setUp(self):
        self.run = GeneralTest()


    def tearDown(self):
        pass


    @ddt.data(*cases("forecast"))
    def test_forecast(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


    @ddt.data(*cases("lifestyle"))
    def test_lifestyle(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


    @ddt.data(*cases(""))
    def test_normal_forecast(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


    @ddt.data(*cases("now"))
    def test_now(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


if __name__ == '__main__':
    unittest.main()
