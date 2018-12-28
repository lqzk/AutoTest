import unittest
from InterfaceAuto.common import ddt
from InterfaceAuto.common.data_handle import DataHandle
from InterfaceAuto.common.general_test import GeneralTest
from InterfaceAuto.common.json_handle import JmespathExtractor
import json
JExtractor = JmespathExtractor()
project = "Risk_assess"
module = "flow"
module_cases=DataHandle().obtain_interface_cases(project, table_name=module)
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
        if case_data["Module"]=="znys" and case_data["Interface"]=="next/question" and not case_data.get("Run")=="N":
            self.run.execute_case(table_result)
            case_data["tags"] = []
            case_data["tags"].extend(json.loads(case_data["Input"]["tags"]))
            from InterfaceAuto.common.call_api import CallAPI
            res_keys=list(table_result[-1]["Res"]["data"].keys())
            while not res_keys==["record_id"]:
                input = table_result[-1]["Input"]
                input["qid"] = JExtractor.extract("Res.data.questions", table_result[-1])[0]["id"]
                input["record_id"] = JExtractor.extract("Res.data.record_id", table_result[-1])
                tag0=JExtractor.extract("Res.data.questions", table_result[-1])[0]["choice_tags"][0]
                tag_list=[]
                tag_list.append(tag0)
                case_data["tags"].append(tag0)
                input["tags"] = json.dumps(tag_list)
                Response = CallAPI().run(method=case_data["method"], url=case_data["Url"], input=input,
                                         headers=case_data.get("headers"), files=case_data.get("files"))
                case_data["Res"] = Response["res"]
                case_data["Res_headers"] = Response["Res_headers"]
                case_data["Res_time(s)"] = Response["res_time"]
                case_data["status_code"]=Response["status_code"]
                res_keys = list(table_result[-1]["Res"]["data"].keys())
            print("最终值：{0}\n".format(case_data))
        else:
            self.run.execute_case(table_result)








if __name__ == '__main__':
    unittest.main()
