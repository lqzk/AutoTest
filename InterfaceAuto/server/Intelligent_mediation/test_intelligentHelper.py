import unittest
import ddt
from InterfaceAuto.common.data_handle import DataHandle,project_case_data
from InterfaceAuto.common.general_test import GeneralTest

project = "Intelligent_mediation"
module = "intelligentHelper"
cases=lambda interface: DataHandle().obtain_interface_cases(project, module, interface)
case_result=project_case_data(project,module)


@ddt.ddt
class TestIntelligentHelper(unittest.TestCase):

    def setUp(self):
        self.run=GeneralTest()

    def tearDown(self):
        pass

    @ddt.data(*cases("similarInfo"))
    def test_similarInfo(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


    @ddt.data(*cases("similarLaw"))
    def test_similarLaw(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


    @ddt.data(*cases("strategy"))
    def test_strategy(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data