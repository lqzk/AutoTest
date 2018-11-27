import unittest
import ddt
from InterfaceAuto.common.data_handle import DataHandle,project_case_data
from InterfaceAuto.common.general_test import GeneralTest

project = "Intelligent_mediation"
module = "mediate"
cases=lambda interface: DataHandle().obtain_interface_cases(project, module, interface)
case_result=project_case_data(project,module)



@ddt.ddt
class TestCase(unittest.TestCase):

    def setUp(self):
        self.run=GeneralTest()

    def tearDown(self):
        pass

    @ddt.data(*cases("getCaseInfo"))
    def test_getCaseInfo(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data

    @ddt.data(*cases("getFullCaseInfo"))
    def test_getFullCaseInfo(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


    @ddt.data(*cases("getParties"))
    def test_getParties(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data


    @ddt.data(*cases("quick/saveCaseInfo"))
    def test_quick_saveCaseInfo(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data

    @ddt.data(*cases("quick/saveCompany"))
    def test_quick_saveCompany(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data

    @ddt.data(*cases("quick/saveNatural"))
    def test_quick_saveNatural(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data

    @ddt.data(*cases("quick/saveResult"))
    def test_quick_saveResult(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data

    @ddt.data(*cases("uploadFile"))
    def test_uploadFile(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data

    @ddt.data(*cases("written/saveCaseInfo"))
    def test_written_saveCaseInfo(self,case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data=case_data

    @ddt.data(*cases("written/saveCompany"))
    def test_written_saveCompany(self, case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data = case_data

    @ddt.data(*cases("written/saveNatural"))
    def test_written_saveNatural(self, case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data = case_data

    @ddt.data(*cases("written/saveResult"))
    def test_written_saveResult(self, case_data):
        try:
            self.run.execute_case(case_data)
        except Exception as e:
            raise Exception(e)
        finally:
            case_result.data = case_data



if __name__ == '__main__':
    unittest.main()
