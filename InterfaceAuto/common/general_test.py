import unittest
from InterfaceAuto.common.call_api import CallAPI
import re
from InterfaceAuto.common.json_extractor import JmespathExtractor
JExtractor = JmespathExtractor()



class GeneralTest(unittest.TestCase):
    #加工单个接口用例的测试数据,主要是输入、预期数据的加工提取
    def handle_case_data(self,case_data):

        input_data = {}
        except_info=[]

        #加工Input数据
        input=case_data["Input"]

        if input=="":
            input_data=None
        else:
            input_list=input.strip().split("\n")
            for every_input in input_list:
                parse_input=every_input.split("=")
                input_data[parse_input[0]]=parse_input[1]


        #加工CaseExcept数据,并获取验证数据，其格式
        # {"验证方式，如equal，contains"：
        #                         {"验证对象获取方式":"验证数值"}}



        interface_except=""
        for iexcept in case_data["interface_except"] :

            iexcept=iexcept.strip()
            if  not iexcept=="":
                interface_except=interface_except+iexcept+"\n"
        case_data["interface_except"] =interface_except

        case_except=interface_except+case_data["CaseExcept"]


        if not case_except=="":
            case_except_list=case_except.strip().split("\n")

            for case_except in case_except_list:
                obtain_obj_method = re.search(r'(.*?)\[', case_except).group(1)
                check_method = re.search(r'\[(.*?)\]', case_except).group(1)
                check_value = re.search(r'\](.*?)$', case_except).group(1)

                if re.search(r'\{(.*?)\}', check_value):
                    obtain_value = re.search(r'\{(.*?)\}', check_value).group(1)
                    if obtain_value in input_data.keys():
                        check_value = input_data[obtain_value]

                if check_value.isnumeric() and len(check_value)<10 and check_value[0]!="0" :
                    check_value = int(check_value)

                except_info.append((obtain_obj_method, check_method, check_value))

        return (input_data,except_info)



    def check_result(self,response,check_infos):

        for check_info in check_infos:
            try:

                check_method = check_info[1]

                # 根据check_method区别验证
                if check_method == "=":
                    check_obj = JExtractor.extract(check_info[0], response)
                    check_value = check_info[2]
                    self.assertEqual(check_value, check_obj)


                elif check_method == "contains":
                    check_obj = JExtractor.extract(check_info[0], response)
                    check_value = check_info[2]
                    if isinstance(check_obj, list):
                        for obj in check_obj:
                            self.assertIn(check_value, obj)
                    else:
                        self.assertIn(check_value, check_obj)

                elif check_method == "type":
                    check_obj = JExtractor.extract(check_info[0], response)
                    check_value = check_info[2]
                    if check_value == "list":
                        self.assertTrue(isinstance(check_obj, list))
                    elif check_value == "dict":
                        self.assertTrue(isinstance(check_obj, dict))
                    elif check_value == "tuple":
                        self.assertTrue(isinstance(check_obj, tuple))

                elif check_method == "len":
                    check_obj = JExtractor.extract(check_info[0], response)
                    check_value = check_info[2]
                    self.assertEqual(check_value, len(check_obj))


                elif check_method == "key":
                    check_value = check_info[2].split(",")

                    check_obj = JExtractor.extract(check_info[0], response)
                    self.assertTrue(isinstance(check_obj, dict))
                    for value in check_value:
                        self.assertIn(value, check_obj.keys())


                elif check_method == "list_key":
                    check_value = check_info[2].split(",")

                    check_obj = JExtractor.extract(check_info[0], response)
                    self.assertTrue(isinstance(check_obj, list))
                    for check_o in check_obj:
                        for value in check_value:
                            self.assertIn(value, check_o.keys())

                elif check_method == "list_dict":
                    check_value = check_info[2]

                    check_obj_split = check_info[0].split(".")
                    check_obj_list = JExtractor.extract(check_obj_split[0], response)
                    self.assertTrue(isinstance(check_obj_list, list))
                    for check_o in check_obj_list:
                        self.assertTrue(isinstance(check_o, dict))
                        check_obj_dict=check_info[0].replace(check_obj_split[0]+".","")
                        check_obj_dict = JExtractor.extract(check_obj_dict, check_o)
                        self.assertEqual(check_value, check_obj_dict)


                elif check_method == "dict_list_dict":
                    check_value = check_info[2]

                    check_obj_split = check_info[0].split(".")
                    check_obj_list = JExtractor.extract("{0}.{1}".format(check_obj_split[0],check_obj_split[1]), response)
                    self.assertTrue(isinstance(check_obj_list, list))
                    for check_o in check_obj_list:
                        self.assertTrue(isinstance(check_o, dict))
                        check_obj_dict=check_info[0].replace("{0}.{1}.".format(check_obj_split[0],check_obj_split[1]),"")
                        check_obj_dict = JExtractor.extract(check_obj_dict, check_o)
                        self.assertEqual(check_value, check_obj_dict)


                elif check_method == "list_dict_key":
                    check_value = check_info[2].split(",")

                    check_obj_split = check_info[0].split(".")
                    check_obj_list = JExtractor.extract(check_obj_split[0], response)
                    self.assertTrue(isinstance(check_obj_list, list))
                    for check_o in check_obj_list:
                        self.assertTrue(isinstance(check_o, dict))
                        check_obj_dict = JExtractor.extract(check_obj_split[1], check_o)
                        for value in check_value:
                            self.assertIn(value, check_obj_dict.keys())


                elif check_method == "list_list_key":
                    check_value = check_info[2].split(",")

                    check_obj_split = check_info[0].split(".")
                    check_obj_list_1 = JExtractor.extract(check_obj_split[0], response)
                    self.assertTrue(isinstance(check_obj_list_1, list))
                    for check_o1 in check_obj_list_1:
                        self.assertTrue(isinstance(check_o1, dict))
                        check_obj_list_2 = JExtractor.extract(check_obj_split[1], check_o1)
                        self.assertTrue(isinstance(check_obj_list_1, list))
                        for check_o2 in check_obj_list_2:
                            self.assertTrue(isinstance(check_o2, dict))
                            for value in check_value:
                                self.assertIn(value, check_o2.keys())
            except Exception as e:
                raise Exception("验证check_info失败：{0}，error info：{1}\n".format(check_info,e))

    def execute_case(self,case_data):

        if case_data["Run"]=="Y":
            print("**************************Start测试用例：{0}*********************************".format(case_data["用例描述"]))

            print("请求方式:{0},   请求地址：{1}".format(case_data["method"], case_data["url"]))
            input_and_except_info=self.handle_case_data(case_data)

            handle_input=input_and_except_info[0]
            handle_except_info=input_and_except_info[1]
            print("测试输入:{0},   期望输出：{1}".format(handle_input,handle_except_info))
            res = CallAPI().run(method=case_data["method"], url=case_data["url"], input=handle_input)
            print("测试实际返回值：\n{0}".format(res))
            case_data["response"] = res

            try:
                self.check_result(res, handle_except_info)
                case_data["Result"] = "True"
                case_data["Error_msg"] = ""
            except Exception as e:
                case_data["Result"] = "False"
                case_data["Error_msg"] = e
                raise Exception(e)

            print("**************************PASS测试用例：{0}**********************************\n\n".format(
                case_data["用例描述"]))
        else:
            self.handle_case_data(case_data)
            print("skip and No Run")



