import unittest
from InterfaceAuto.common import ddt
from InterfaceAuto.common.data_handle import DataHandle
from InterfaceAuto.common.general_test import GeneralTest
project = "Intelligent_mediation"

dispute_flow_table = "dispute_flow"
dispute_flow_cases=DataHandle().obtain_interface_cases(project, table_name=dispute_flow_table)
dispute_flow_result=[]


quick_dispute_flow_table = "quick_dispute_flow"
quick_dispute_flow_cases=DataHandle().obtain_interface_cases(project, table_name=quick_dispute_flow_table)
quick_dispute_flow_result=[]


written_dispute_flow_table = "written_dispute_flow"
written_dispute_flow_cases=DataHandle().obtain_interface_cases(project, table_name=written_dispute_flow_table)
written_dispute_flow_result=[]


record_flow_table = "record_flow"
record_flow_cases=DataHandle().obtain_interface_cases(project, table_name=record_flow_table)
record_flow_result=[]




@ddt.ddt
class TestCase(unittest.TestCase):
    '''验证业务流程，由于业务关联原因，发生错误只需查看第一个错误接口'''

    def setUp(self):
        self.run=GeneralTest()

    def tearDown(self):
        pass

    @ddt.data(*dispute_flow_cases)
    def test_dispute_flow_cases(self,case_data):
        dispute_flow_result.append(case_data)
        self.run.execute_case(dispute_flow_result)



    @ddt.data(*quick_dispute_flow_cases)
    def test_quick_dispute_flow_cases(self, case_data):
        quick_dispute_flow_result.append(case_data)
        self.run.execute_case(quick_dispute_flow_result)


    @ddt.data(*record_flow_cases)
    def test_record_flow_cases(self, case_data):
        record_flow_result.append(case_data)
        self.run.execute_case(record_flow_result)



    @ddt.data(*written_dispute_flow_cases)
    def test_written_dispute_flow_cases(self, case_data):
        written_dispute_flow_result.append(case_data)
        self.run.execute_case(written_dispute_flow_result)





if __name__ == '__main__':
    unittest.main()
