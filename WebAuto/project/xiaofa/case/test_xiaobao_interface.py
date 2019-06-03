from InterfaceAuto.common.call_api import CallAPI
import ddt
import unittest
import json
from WebAuto.common.excel_data import Excel_Data
from WebAuto.common.data_handle import PATH
question_data=Excel_Data(PATH("project\\xiaofa\\小法测试用例数据.xlsx"),"劳动争议").data
# question_data=[{"title":"我要离婚"},{"title":"符合计划生育规定安排生育的女职工的产假及工资待遇如何规定？"}]

@ddt.ddt
class XiaobaoInterface(unittest.TestCase):
    def setUp(self):
        self.api=CallAPI()
        self.url="http://xiaofa.aegis-info.com/api/law_inference/simple/orion"
        self.parm={}
        self.parm["sn"]="1111"
        self.parm["user_semantics"] = {"deviceid":"aegislawpush"}
        self.parm["query"]=""
        self.res_time_limit=0.5
        self.res_data={}

    def one_run_interface(self,query_data):
        self.parm["query"] = query_data
        print("情形：{0}".format(self.parm["query"]))
        parm_string = json.dumps(self.parm)
        res = self.api.run("post", self.url, parm_string)
        res_data = res["res"]
        print("响应结果：{0}".format(res_data))
        print("响应时间：{0}".format(res["res_time"]))
        try:
            self.assertNotIn("请求次数已达上限", res_data["msg"])
            self.assertIsNotNone(res_data["nlp"][0]["answer"])
            self.assertLessEqual(res["res_time"], self.res_time_limit)
        except Exception as e:
            print("校验结果:{0}".format(e))
            raise Exception(e)

        print("------------------------------------------------------")
        return res_data

    @ddt.data(*question_data)
    def test_xiaofa_interface(self,case_data):
        self.res_data=self.one_run_interface(case_data["title"])
        while self.res_data["nlp"][0].get("card"):
            self.res_data=self.one_run_interface(self.res_data["nlp"][0]["card"]["button"][0]["text"])




if __name__ == '__main__':
    unittest.main()
















