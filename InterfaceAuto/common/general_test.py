import unittest
from InterfaceAuto.common.call_api import CallAPI
import re
import warnings
from collections import Counter
from InterfaceAuto.common.data_handle import DataHandle
from InterfaceAuto.common.json_handle import JmespathExtractor
JExtractor = JmespathExtractor()


class GeneralTest(unittest.TestCase):

    def assert_result(self,check_obj,check_method,check_value):

        if check_method == "=":
            if type(check_value)==type(check_obj):
                self.assertEqual(check_value, check_obj)
            elif isinstance(check_obj, list):
                for check_ob in check_obj:
                    self.assertEqual(check_value, check_ob)
            else:
                self.assertEqual(check_value, check_obj)

        elif check_method == "<":
            self.assertLess(check_obj, check_value)

        elif check_method == "<=":
            self.assertLessEqual(check_obj, check_value)

        elif check_method == ">":
            self.assertGreater(check_obj, check_value)

        elif check_method == ">=":
            self.assertGreaterEqual(check_obj, check_value)

        elif check_method == "C=":
            if isinstance(check_obj, dict) and isinstance(check_value, dict):
                for key1, value1 in check_obj.items():
                    if value1==None:
                        continue
                    else:
                        for key2, value2 in check_value.items():
                            if value2==None:
                                continue
                            elif key1 == key2:
                                self.assertEqual(value1, value2)
                                break
            elif isinstance(check_obj, list):
                self.assertIn(check_value,check_obj)

        elif check_method == "DO=":
            self.assertEqual(type(check_obj),type(check_value))
            if isinstance(check_obj, list):
                if isinstance(check_obj[0], list):
                    for check_ob in check_obj:
                        if isinstance(check_ob[0], list):
                            for check_o in check_ob:
                                self.assertEqual(Counter(check_o), Counter(check_value))
                        else:
                            self.assertEqual(Counter(check_ob), Counter(check_value))
                elif isinstance(check_obj[0], dict):
                    key1=list(check_obj[0].keys())[0]
                    check_obj=sorted(check_obj,key=lambda x:x[key1])
                    check_value = sorted(check_value, key=lambda x:x[key1])
                    self.assertEqual(len(check_obj),len(check_value))
                    for i in range(len(check_obj)):
                        self.assertEqual(check_obj[i],check_value[i])
                else:
                    self.assertEqual(Counter(check_obj), Counter(check_value))

        elif check_method == "!=":
            self.assertNotEqual(check_value, check_obj)

        elif check_method == "len":
            self.assertEqual(check_value, len(check_obj))

        elif check_method == "contains":
            self.assertIn(check_value, check_obj)

        elif check_method == "key":
            if isinstance(check_value,str):
                check_value = check_value.split(",")

            if isinstance(check_obj,list) :
                for every_check_obj in check_obj:
                    if isinstance(every_check_obj, list):
                        for every_check_ob in every_check_obj:
                            try:
                                self.assertEqual(Counter(check_value), Counter(every_check_ob.keys()))
                            except Exception as e:
                                different = Counter(check_value) - Counter(every_check_ob.keys())
                                if list(different)==[]:
                                    different = Counter(every_check_ob.keys())-Counter(check_value)
                                    raise Exception("检查对象多出key值：{0},check_obj实际返回key值为:{1}".format(list(different), list(every_check_ob.keys())))
                                else:
                                    raise Exception("检查对象缺少key值：{0},check_obj实际返回key值为:{1}".format(list(different), list(every_check_ob.keys())))
                    else:
                        try:
                            self.assertEqual(Counter(check_value), Counter(every_check_obj.keys()))
                        except Exception as e:
                            different = Counter(check_value) - Counter(every_check_obj.keys())
                            if list(different) == []:
                                different = Counter(every_check_obj.keys()) - Counter(check_value)
                                raise Exception("检查对象多出key值：{0},check_obj实际返回key值为:{1}".format(list(different), list(every_check_obj.keys())))
                            else:
                                raise Exception("检查对象缺少key值：{0},check_obj实际返回key值为:{1}".format(list(different), list(every_check_obj.keys())))
            else:
                try:
                    self.assertEqual(Counter(check_value), Counter(check_obj.keys()))
                except Exception as e:
                    different = Counter(check_value) - Counter(check_obj.keys())
                    if list(different) == []:
                        different = Counter(check_obj.keys()) - Counter(check_value)
                        raise Exception("检查对象多出key值：{0},check_obj实际返回key值为:{1}".format(list(different),list(check_obj.keys())))
                    else:
                        raise Exception("检查对象缺少key值：{0},check_obj实际返回key值为:{1}".format(list(different),list(check_obj.keys())))

        elif check_method == "Ckey":
            if isinstance(check_value, str):
                check_value = check_value.split(",")

            if isinstance(check_obj, list):
                for every_check_obj in check_obj:
                    for check_v in check_value:
                        self.assertIn(check_v, every_check_obj.keys())

            else:
                for check_v in check_value:
                    self.assertIn(check_v, check_obj.keys())

        elif check_method == "type":
            if check_value == "list":
                self.assertIsInstance(check_obj, list)
                # self.assertTrue(isinstance(check_obj, list))
            elif check_value == "dict":
                self.assertIsInstance(check_obj, dict)
                # self.assertTrue(isinstance(check_obj, dict))

        elif check_method == "mode":
            # self.assertTrue(re.search(check_value,check_obj))
            self.assertRegex(check_obj,check_value)
        else:
            raise Exception("不存在的校验方式：{0}".format(check_method))

    def check_result(self,table_result,check_infos):
        case_data = table_result[-1]

        quoto_situation = case_data["QuotoSituation"]
        if quoto_situation != None:
            for k,v in quoto_situation.items():
                v = DataHandle().obtain_quote_data(v, table_result)
                v = DataHandle().handle_string_obj(v)
                if isinstance(v, str) and re.search(r'&extract\[(.*?)]$', v):
                    pattern=re.search(r'&extract\[(.*?)]$', v).group(1)
                    v=re.search(pattern,v).group(1)
                quoto_situation[k] = v
            case_data["QuotoSituation"]=quoto_situation


        for check_info in check_infos:
            try:
                quary_string=check_info[0]
                check_des = check_info[1]
                check_value= check_info[2]

                check_des= DataHandle().obtain_quote_data(check_des, table_result)
                check_des=DataHandle().obtain_QuotoSituation_data(case_data["project"],quoto_situation,check_des)

                check_des_list=check_des.split(",")
                location_list=None
                if len(check_des_list)==1:
                    check_obj_type, check_method = "default", check_des_list[0]
                elif len(check_des_list)==2:
                    check_obj_type, check_method = check_des_list[0],check_des_list[1]
                elif len(check_des_list)==3:
                    check_obj_type, check_method,location_des = check_des_list[0], check_des_list[1],check_des_list[2]
                    location_list=location_des.split("@")
                else:
                    raise Exception("check_info:{0},验证格式错误:{1}".format(check_info,check_des))

                if re.search(r'\%(.*?)\%', quary_string):
                    check_obj=DataHandle().obtain_QuotoSituation_data(case_data["project"],quoto_situation,quary_string,check_obj_type,location_list)
                elif re.search(r'\<(.*?)\>', quary_string):
                    check_obj=DataHandle().obtain_quote_data(quary_string,table_result)
                else:
                    check_obj = DataHandle().obtain_type_data(quary_string, check_obj_type, case_data["Res"], location_list)

                check_value=DataHandle().obtain_QuotoSituation_data(case_data["project"],quoto_situation,check_value)

                try:
                    self.assert_result(check_obj, check_method, check_value)
                    print("校验该段信息成功：{0}".format(check_info))
                except Exception as e:
                    print("校验该段信息失败：{0}".format(check_info))
                    raise Exception("校验该段信息失败：{0}，error info：{1}\n".format(check_info, e))

            except Exception as e:
                raise Exception("case_data：{0}\n\n\n验证check_info失败：{1}，error info：{2}\n".format(case_data,check_info,e))

    def execute_case(self,table_result):

        case_data=table_result[-1]
        warnings.simplefilter("ignore", ResourceWarning)

        if case_data.get("Run")!="N":
            # print(case_data)
            print("**************************Start测试用例：{0}*********************************".format(case_data["用例描述"]))

            table_result = DataHandle().handle_case_data(table_result)

            handle_input = case_data["handle_Input"]
            handle_except_info = case_data["CaseExcept"]
            handle_url = case_data["Url"]
            handle_headers = case_data.get("headers")
            handle_files = case_data.get("files")
            time_out=case_data.get("timeout")

            print("请求方式:{0},   请求地址：{1}".format(case_data["method"], handle_url))
            print("测试输入:{0}、{1}、{2}".format(case_data["Input"], handle_headers, handle_files))
            print("期望输出：{0}".format(handle_except_info))
            Response = CallAPI().run(method=case_data["method"], url=handle_url, input=handle_input,
                                     headers=handle_headers, files=handle_files,time_out=time_out)
            del case_data["handle_Input"]

            print("测试实际返回值：\n{0}".format(Response["res"]))
            case_data["Res"] = Response["res"]
            case_data["Res_headers"] = Response["Res_headers"]
            case_data["Res_time"] = Response["res_time"]
            case_data["status_code"] = Response["status_code"]

            self.check_result(table_result, handle_except_info)

            print("**************************PASS测试用例：{0}**********************************\n\n".format(case_data.get("用例描述")))
        else:
            print("skip and No Run")




