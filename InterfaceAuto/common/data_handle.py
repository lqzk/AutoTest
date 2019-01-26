from InterfaceAuto.common.json_handle import JsonHandle
from InterfaceAuto.common.excel_data import Excel_Data
import os
import json
import re
import glob
import  time
import copy
from ast import literal_eval
from InterfaceAuto.common.json_handle import JmespathExtractor
JExtractor = JmespathExtractor()

#p="common\\path_handle.py"即从项目一级目录开始
PATH=lambda P:os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),P))
dir_report_path=PATH("report\\")
email_config_path=PATH("data\\email_config.ini")
email_list=JsonHandle(PATH("data\\email_list.json")).jData
project_case_path=lambda p:PATH("server\\{0}".format(p))


project_case_data=lambda p,f,m:Excel_Data(PATH("server\\{0}\\{1}.xlsx".format(p,f)),m)
prefix_url_path=PATH("data\\interface_info.json")
case_exeorder_path=PATH("data\\case_exeorder.xlsx")
comparison_list_path=PATH("data\\comparison_list.json")



class DataHandle:
    
    def obtain_email_config(self,project_name=None):
        email_config_info={}
        suffix_config_file=os.path.splitext(email_config_path)[1]
        key="email"
        if project_name:
            key="{0}_email".format(project_name)
        if suffix_config_file==".ini":
            import configparser
            email_config=configparser.ConfigParser()
            email_config.read(email_config_path,encoding="utf-8")
            email_config_info["server"]=email_config.get(key,"server")
            email_config_info["sender"] = email_config.get(key, "sender")
            email_config_info["password"] = email_config.get(key, "password")
            email_config_info["receiver"] = eval(email_config.get(key, "receiver"))
            email_config_info["title"] = email_config.get(key, "title")
            email_config_info["message"] = email_config.get(key, "message")
            email_config_info["attachment_path"]=self.obtain_newest_report()

        elif suffix_config_file==".json":
            email_config_info=JsonHandle(email_config_path).jData
            email_config_info["attachment_path"] = self.obtain_newest_report()

        return email_config_info

    def obtain_newest_report(self):
        file_list=os.listdir(dir_report_path)
        del file_list[-1]
        newest_file_path=sorted(glob.glob(os.path.join(dir_report_path, '*')),key=lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(x))), reverse=True)[0]
        return newest_file_path

    def obtain_case_exe_order(self,project):
        test_case_list=[]
        exeorder_data = Excel_Data(case_exeorder_path, project).data
        for every_data in exeorder_data:
            if every_data["Run"] == "Y":
                test_case = "{0}('{1}')".format(every_data["ClassName"].strip(),
                                                every_data["Case"].strip())
                test_case_list.append(test_case)
        return test_case_list

    def obtain_import_cases_statement(self,project):
        dir_cases=project_case_path(project)
        import_statement = ""
        for root, dirs, files in os.walk(dir_cases):
            from_str = ""
            from_list = root.split("\\")[2:]
            for l in from_list:
                from_str = from_str + l + "."
            from_obj = from_str[:-1]
            import_strs = ""
            for f in files:
                if f[:5] == "test_" and f[-3:] == ".py":
                    import_strs = import_strs + f[:-3] + ","
            import_objs = import_strs[:-1]
            import_statement = "from " + from_obj + " import " + import_objs
            break
        return import_statement

    #解析并获取json文件里面的接口信息数据
    def obtain_interface_info(self,project,module,interface):
        prefix_url_data = JsonHandle(prefix_url_path).jData

        if not prefix_url_data.get(project):
            print("未找到项目：{0}".format(project))
            raise Exception("未找到项目：{0}".format(project))
        elif not prefix_url_data[project].get(module):
            print("{0}该项目下未找到模块：{1}".format(project, module))
            raise Exception("{0}该项目下未找到模块：{1}".format(project, module))
        elif not prefix_url_data[project][module].get(interface):
            print("{0}该模块下未找到接口：{1}".format(module, interface))
            raise Exception("{0}该模块下未找到接口：{1}".format(module, interface))
        else:
            handle_interface_info = {}
            project_info=prefix_url_data[project]
            module_info=project_info[module]
            interface_info=module_info[interface]

            handle_interface_info["timeout"]=project_info.get("base_timeout")

            handle_interface_info["method"]=interface_info.get('method')
            handle_interface_info["base_url"] = project_info["base_url"]

            handle_interface_info["Url"] = project_info["base_url"]+module_info["module_url"]+interface
            handle_interface_info["Interface_description"] = "【{0}】{1}".format(module_info["module_description"],
                                                                               interface_info["interface_description"])
            handle_interface_info["headers"] = interface_info.get("headers")


            interface_except=project_info["base_except"]
            interface_except.extend(module_info["module_except"])
            interface_except.extend(interface_info["interface_except"])
            handle_interface_info["Interface_except"] = interface_except

            leader=[]
            leader.append(project_info.get("base_leader"))
            leader.append(module_info.get("module_leader"))
            leader.append(interface_info.get("interface_leader"))
            while None in leader:
                leader.remove(None)
            while "" in leader:
                leader.remove("")
            if not leader==[]:
                handle_interface_info["leader"]=",".join(leader)
            else:
                handle_interface_info["leader"]=None

        return handle_interface_info

    # 解析并获取excel文件里面的某模块单接口全部测试用例，或者获取某表全部测试用例
    def obtain_interface_cases(self,project,module=None,table_name=None,table_index=None,sun_project=None):
        case_list = []
        if sun_project==None:
            sun_project=project

        if module != None:
            interface_list_info = {}
            interface_list = project_case_data(project,sun_project,module).getSingleColumnType("Interface")
            for interface in interface_list:
                interface_info = self.obtain_interface_info(sun_project, module, interface)
                interface_list_info[interface] = interface_info

            data_list = project_case_data(project,sun_project,module).data
            for data in data_list:
                data["project"] = project
                data["result_table_name"] = module
                data.update(interface_list_info[data["Interface"]])
                case_list.append(data)
        else:
            data_list = project_case_data(project,sun_project,table_name).data
            if table_index == None:
                interface_list_info = {}
                m_interface_list = project_case_data(project,sun_project,table_name).getDoubleColumnType("Module","Interface")
                for m_interface in m_interface_list:
                    interface_info = self.obtain_interface_info(sun_project, m_interface[0], m_interface[1])
                    interface_list_info["{0}_{1}".format(m_interface[0], m_interface[1])] = interface_info

                for data in data_list:
                    data["project"] = project
                    data["result_table_name"] = table_name
                    data.update(interface_list_info["{0}_{1}".format( data["Module"], data["Interface"])])
                    case_list.append(data)
            else:
                data=data_list[table_index-1]
                data["project"] = project
                data["result_table_name"] = table_name
                if data.get("Module")==None:
                    module=table_name
                else:
                    module=data["Module"]
                interface_info = self.obtain_interface_info(sun_project, module, data["Interface"])
                data.update(interface_info)
                case_list.append(data)
        return case_list

    #将字符串类型数据转为应是的数据格式
    def handle_string_obj(self,string_obj):
        if isinstance(string_obj,str):
            try:
                if re.search(r'^dumps\{(.*?)\}$', string_obj):
                    string_obj=re.search(r'^dumps(\{.*?\})$', string_obj).group(1)
                    obtain_value = json.loads(string_obj)
                    obtain_value = json.dumps(obtain_value)
                elif re.search(r'^dumps\[(.*?)\]$', string_obj):
                    string_obj=re.search(r'^dumps(\[.*?\])$', string_obj).group(1)
                    obtain_value = json.loads(string_obj)
                    obtain_value = json.dumps(obtain_value)
                elif re.search(r'^\{(.*?)\}$', string_obj):
                    string_obj = string_obj.replace("\'", "\"")
                    string_obj = string_obj.replace("None", "null")
                    obtain_value = json.loads(string_obj)
                elif re.search(r'^\[(.*?)\]$', string_obj):
                    obtain_value = literal_eval(string_obj)
                elif re.search(r'int\(([0-9]*?)\)', string_obj):
                    string_int = re.search(r'int\(([0-9]*?)\)', string_obj).group(1)
                    obtain_value = int(string_int)
                elif re.search(r'double\((.*?)\)', string_obj):
                    string_int = re.search(r'double\((.*?)\)', string_obj).group(1)
                    obtain_value = float(string_int)
                else:
                    obtain_value = string_obj
                return obtain_value
            except Exception as e:
                raise Exception("无法转化该数据：{0}，error_info:{1}".format(string_obj, e))
        return string_obj

    # 获取格式解码后数据，按照获取字符串、规定的格式公式、获取值
    def obtain_type_data(self, quary_string, quary_type_string, quary_origin_value,location=None):
        if isinstance(quary_origin_value,dict):
            quary_value = copy.deepcopy(quary_origin_value)
            if quary_string == "all":
                return quary_value
            else:
                quary_string_list = quary_string.split(".")
                i = 0
                for quary_value_type in quary_type_string.split("_"):
                    if re.search(r'dict([0-9]*?)$', quary_value_type):
                        dict_number = re.search(r'dict([0-9]*?)$', quary_value_type).group(1)
                        if dict_number == "":
                            dict_number = 1
                            quary_string = quary_string_list[i]
                        else:
                            dict_number = int(dict_number)
                            quary_string = '.'.join(quary_string_list[i: i + dict_number])

                        if isinstance(quary_value, list):
                            for j in range(len(quary_value)):
                                quary_value[j] = JExtractor.extract(quary_string, quary_value[j])
                        elif isinstance(quary_value, dict):
                            quary_value = JExtractor.extract(quary_string, quary_value)

                        i = i + dict_number
                    elif re.search(r'list([0-9]*?)$', quary_value_type):
                        list_number = re.search(r'list([0-9]*?)$', quary_value_type).group(1)
                        if isinstance(quary_value, dict):
                            quary_value = JExtractor.extract(quary_string_list[i], quary_value)
                            if list_number == "":
                                if location != None:
                                    break_flag = False
                                    for dict_quary_value in quary_value:
                                        for key, value in dict_quary_value.items():
                                            if key == location[0] and value == location[1]:
                                                quary_value = dict_quary_value
                                                break_flag = True
                                                break
                                        if break_flag == True:
                                            break
                            else:
                                list_number = int(list_number)
                                quary_value = quary_value[list_number]

                        elif isinstance(quary_value, list):
                            for j in range(len(quary_value)):
                                if list_number == "":
                                    quary_value[j] = JExtractor.extract(quary_string_list[i], quary_value[j])
                                else:
                                    list_number = int(list_number)
                                    quary_value[j] = JExtractor.extract(quary_string_list[i], quary_value[j])[
                                        list_number]
                        i = i + 1
                    elif quary_value_type == "default":
                        if len(quary_string_list) == 1:
                            quary_value = quary_value[quary_string]
                        else:
                            quary_string = '.'.join(quary_string_list)
                            quary_value = JExtractor.extract(quary_string, quary_value)
                return quary_value

    def transfer_obj(self,project,handle_des,transfer_value):
        if re.search(r'(.*?)\[', handle_des):
            handle_operation = re.search(r'(.*?)\[', handle_des).group(1)
            handle_mode = re.search(r'\[(.*?)\]', handle_des).group(1)
            if handle_operation == "transfer":
                with open(comparison_list_path, "rb"):
                    comparison_list_data = JsonHandle(comparison_list_path).jData[project]
                for key1, value1 in comparison_list_data.items():
                    if key1 == handle_mode:
                        for key2, value2 in value1.items():
                            if key2 == transfer_value:
                                transfer_value = value2
                                break
                            if value2 == transfer_value:
                                transfer_value = key2
                                break
                        break
                else:
                    raise Exception("无法找到转化对象：{0}".format(handle_mode))
                transfer_value = self.handle_string_obj(transfer_value)
        return transfer_value

    # 获取引用的数据按照提供的引用信息
    def obtain_quote_data(self, quote_string_value,table_result):
        try:
            if isinstance(quote_string_value, str) and re.search(r'\<(.*?)\>', quote_string_value):
                case_data = table_result[-1]
                case_num = None
                quote_value = None
                handle_des = None
                case = None
                quote_string_list=re.findall(r'\<(.*?)\>', quote_string_value)
                for quote_string in quote_string_list:
                    obtain_value_method =quote_string.split(",")

                    if len(obtain_value_method) == 1:
                        obtain_value = obtain_value_method[0]

                        if case_data.get(obtain_value):
                            quote_value = case_data[obtain_value]
                        elif case_data["Input"].get(obtain_value):
                            quote_value = case_data["Input"][obtain_value]
                        else:
                            raise Exception("无法找到obtain_value：{0}".format(obtain_value))

                    elif len(obtain_value_method) == 2:
                        res=case_data.get("Res")
                        if res==None:
                            continue
                        else:
                            value_key = obtain_value_method[1]
                            quote_value_type, quary_string = "default", value_key
                            location_list=None
                            if re.search(r'\[(.*?)\]', value_key):
                                quote_value_des = re.search(r'\[(.*?)\]', value_key).group(1)
                                quary_string = re.search(r'(.*?)\[', value_key).group(1)
                                quote_value_des = quote_value_des.split("/")
                                if len(quote_value_des) == 1:
                                    quote_value_type = quote_value_des[0]
                                elif len(quote_value_des) == 2:
                                    quote_value_type, location_des = quote_value_des[0], quote_value_des[1]
                                    if isinstance(location_des, str):
                                        location_list = location_des.split("@")
                                        location_list[1] = self.obtain_QuotoSituation_data(case_data["project"],case_data["QuotoSituation"],
                                                                                           location_list[1])

                            quote_value = self.obtain_type_data(quary_string, quote_value_type, res,
                                                                location_list)

                    elif len(obtain_value_method) == 3:
                        case_num, value_type, value_key = obtain_value_method[0], obtain_value_method[1],obtain_value_method[2]

                    elif len(obtain_value_method) == 4:
                        case_num, value_type, value_key, handle_des = obtain_value_method[0],obtain_value_method[1], obtain_value_method[2], obtain_value_method[3]

                    elif len(obtain_value_method)==5:
                        case,case_num, value_type, value_key, handle_des = obtain_value_method[0], obtain_value_method[1], \
                                                                      obtain_value_method[2], obtain_value_method[3],obtain_value_method[4]

                    else:
                        raise Exception("{0}：{1}无匹配的引用格式".format(quote_string_value, obtain_value_method))

                    if len(obtain_value_method) in [3,4,5]:
                        i = int(re.search(r"case([0-9]*?)$", case_num).group(1))
                        if len(obtain_value_method)==5:
                            data_list=self.obtain_interface_cases(case_data["project"],table_name=case,table_index=i)
                            data_list[-1]["Run"]="Y"
                            from InterfaceAuto.common.general_test import GeneralTest
                            GeneralTest().execute_case(data_list)
                            data=data_list[0]
                        else:
                            data = table_result[i - 1]

                        if data.get(value_type):
                            quote_value = self.handle_string_obj(data[value_type])
                            if value_key != "all":
                                quote_value_type, quary_string = "default", value_key
                                location_list = None
                                if re.search(r'\[(.*?)\]', value_key):
                                    quote_value_des = re.search(r'\[(.*?)\]', value_key).group(1)
                                    quary_string = re.search(r'(.*?)\[', value_key).group(1)

                                    quote_value_des = quote_value_des.split("/")
                                    if len(quote_value_des) == 1:
                                        quote_value_type = quote_value_des[0]
                                    elif len(quote_value_des) == 2:
                                        quote_value_type, location_des = quote_value_des[0], quote_value_des[1]
                                        if isinstance(location_des, str):
                                            location_list = location_des.split("@")
                                            location_list[1] = self.obtain_QuotoSituation_data(case_data["project"],case_data["QuotoSituation"],
                                                                                               location_list[1])

                                quote_value = self.obtain_type_data(quary_string, quote_value_type, quote_value,
                                                                    location_list)
                        elif value_type=="all":
                            quote_value=data
                        else:
                            raise Exception("{0}中不存在的key值：{1}".format(data,value_type))



                    if len(obtain_value_method) in [4,5]:
                        if handle_des=="Undo":
                            pass
                        elif re.search("transfer\[(.*?)\]",handle_des):
                            quote_value=self.transfer_obj(case_data["project"],handle_des,quote_value)
                        elif re.search("extract\[(.*?)\]",handle_des):
                            extract_mode = re.search(r'\[(.*?)\]', handle_des).group(1)
                            if re.search(extract_mode,quote_value):
                                quote_value=re.search(extract_mode,quote_value).group(1)
                            else:
                                raise Exception("无法从{0}中按照方式{1}提取值".format(quote_value,extract_mode))
                        else:
                            raise Exception("不符合格式的后续处理方式：{0}".format(handle_des))

                    if quote_string_value=="<{0}>".format(quote_string):
                        quote_string_value=quote_value
                    else:
                        if isinstance(quote_value,str) and (re.search(r'^\{(.*?)\}$', quote_string_value) or re.search(r'^\[(.*?)\]$', quote_string_value)):
                            quote_string_value = quote_string_value.replace("<{0}>".format(quote_string),"'{0}'".format(quote_value))
                        else:
                            quote_string_value=quote_string_value.replace("<{0}>".format(quote_string),str(quote_value))
            return quote_string_value
        except Exception as e:
            raise Exception("从值:{0}获取引用值失败,error_info:{1}".format(quote_string_value,e))

    def obtain_QuotoSituation_data(self,project,quoto_situation_data,quote_string,quote_string_type="default",location=None):

        if isinstance(quote_string, str) and re.search(r'\%(.*?)\%', quote_string):
            try:
                quote_key_list = re.findall(r'\%(.*?)\%', quote_string)

                if len(quote_key_list) == 1 and re.search(r'^\%(.*?)\%[^\]\,\}]',quote_string):
                    quote_key = re.search(r'\%(.*?)\%', quote_string).group(1)
                    quote_value = JExtractor.extract(quote_key, quoto_situation_data)

                    if re.search(r'\%(.*?)\%([a-zA-Z].*?)$', quote_string):
                        if isinstance(quote_value,dict):
                            quote_string = re.search(r'\%(.*?)\%(.*?)$', quote_string).group(2)
                            quote_string_list = quote_string.split("&")
                            if re.search(r'\[(.*?)\]', quote_string_list[0]):
                                quote_string_type = re.search(r'\[(.*?)\]', quote_string_list[0]).group(1)
                                quote_string = re.search(r'(.*?)\[', quote_string_list[0]).group(1)
                            else:
                                quote_string = quote_string_list[0]

                            quote_value = self.obtain_type_data(quote_string, quote_string_type, quote_value,
                                                                location)
                            if len(quote_string_list) == 2:
                                handle_des = quote_string_list[1]
                                if re.search(r"transfer\[(.*?)\]", handle_des):
                                    quote_value = self.transfer_obj(project, handle_des, quote_value)
                                elif re.search("extract\[(.*?)\]", handle_des):
                                    extract_mode = re.search(r'\[(.*?)\]', handle_des).group(1)
                                    if re.search(extract_mode, quote_value):
                                        quote_value = re.search(extract_mode, quote_value).group(1)
                                    else:
                                        raise Exception("无法提取值从{0}中按照方式:{1}".format(quote_value, extract_mode))
                                else:
                                    raise Exception("不符合格式的后续处理方式：{0}".format(handle_des))
                        else:
                            quote_value=quote_string
                        return quote_value
                else:
                    for quote_key in quote_key_list:
                        quote_value = JExtractor.extract(quote_key, quoto_situation_data)
                        if isinstance(quote_value, str) and (
                            re.search(r'^\{(.*?)\}$', quote_string) or re.search(r'^\[(.*?)\]$', quote_string)):
                            quote_string = quote_string.replace("%{0}%".format(quote_key),
                                                                "'{0}'".format(quote_value))
                        else:
                            quote_string = quote_string.replace("%{0}%".format(quote_key), str(quote_value))
                    return quote_string
            except Exception as e:
                raise Exception("【获取引用值失败】引用数据：{0}，引用条件：{1}，引用类型：{2}\nerror_info:{3}".format(quoto_situation_data,quote_string,quote_string_type,e))
        return quote_string

    #加工单个接口用例的测试数据,主要是输入、预期数据的加工提取
    def handle_case_data(self,table_result):
        case_data = table_result[-1]

        # 加工quoto_situation数据
        quoto_situation = case_data.get("QuotoSituation")
        case_data["QuotoSituation"] = {}
        if quoto_situation==None or quoto_situation == "":
            case_data["QuotoSituation"] = None
        else:
            quoto_situation_list = quoto_situation.strip().split("\n")
            for every_quoto_situation in quoto_situation_list:
                quoto_situation_data_key=re.search(r'(.*?)\=', every_quoto_situation).group(1)
                quoto_situation_data_value = re.search(r'\=([^\}].*?)$', every_quoto_situation).group(1)

                quoto_situation_data_value = self.obtain_quote_data(quoto_situation_data_value, table_result)
                quoto_situation_data_value =self.obtain_QuotoSituation_data(case_data["project"],case_data["QuotoSituation"],quoto_situation_data_value)

                case_data["QuotoSituation"][quoto_situation_data_key] = quoto_situation_data_value

        #加工Input数据
        input=case_data["Input"]
        handle_input_data = None
        if input=="":
            input_data=None
        else:
            input_data={}

            input_list=input.strip().split("\n")
            for every_input in input_list:
                input_data_key=re.search(r"^(.*?)\=",every_input).group(1)
                input_data_value=re.search(r"\=([^\}].*?)$",every_input).group(1)

                input_data_value = self.obtain_quote_data(input_data_value, table_result)
                input_data_value=self.obtain_QuotoSituation_data(case_data["project"],case_data["QuotoSituation"],input_data_value)

                if isinstance(input_data_value, str):
                    input_data_value_list = input_data_value.split("+")
                    input_data_value = self.handle_string_obj(input_data_value_list[0])
                    if len(input_data_value_list) > 1:
                        for i in range(1, len(input_data_value_list)):
                            input_data_value_list[i] = self.handle_string_obj(input_data_value_list[i])
                            if type(input_data_value) == type(input_data_value_list[i]):
                                if type(input_data_value) == str:
                                    input_data_value = "{0}{1}".format(input_data_value, input_data_value_list[i])
                                elif type(input_data_value) == int:
                                    input_data_value = input_data_value + input_data_value_list[i]
                                else:
                                    raise Exception("{0}数据格式存在问题".format(input_data_value))

                handle_input_data = input_data

                if "file" in input_data_key and "data\\" in str(input_data_value):
                        if isinstance(input_data_value, list):
                            path_values = []
                            i = 1
                            for path_value in input_data_value:
                                relative_path=re.search(r"data\\(.*?)$",path_value).group(1)
                                path_value="data\\{0}\\{1}".format(case_data["project"],relative_path)
                                filename = "test{0}{1}".format(i, re.search(r'\..*', path_value).group(0))
                                path_values.append((input_data_key, (filename, open(PATH(path_value), "rb"))))
                                i = i + 1
                                case_data["files"]=path_values
                        else:
                            relative_path = re.search(r"data\\(.*?)$", input_data_value).group(1)
                            input_data_value = "data\\{0}\\{1}".format(case_data["project"], relative_path)
                            input_data_value = PATH(input_data_value)
                            filename = "test{0}".format(re.search(r'\..*', input_data_value).group(0))
                            handle_file_value = (filename, open(input_data_value, "rb"))
                            case_data["files"] = {input_data_key: handle_file_value}
                elif "headers" in input_data_key:
                    case_data["headers"] = input_data_value
                elif input_data_key in ["info", "form"]:
                    input_data[input_data_key] = input_data_value
                    handle_input_data= json.dumps(input_data_value)
                elif input_data_key=="Url":
                    case_data["Url"]=input_data_value
                else:
                    input_data[input_data_key]=input_data_value
                    handle_input_data=input_data

        case_data["handle_Input"] = handle_input_data
        case_data["Input"] = input_data



        # 加工预期数据
        except_info = []
        interface_except=""
        for iexcept in case_data["Interface_except"] :
            iexcept=iexcept.strip()
            if not iexcept=="":
                interface_except=interface_except+iexcept+"\n"
        case_data["Interface_except"] =interface_except
        case_except=interface_except+case_data["CaseExcept"]
        if not case_except=="":
            case_except_list=case_except.strip().split("\n")

            for case_except in case_except_list:
                try:
                    obtain_obj_method = re.search(r'(.*?)\[', case_except).group(1)
                    check_method = re.search(r'\[(.*?)\]', case_except).group(1)
                    check_value = re.search(r'\](.*?)$', case_except).group(1)
                except Exception as e:
                    raise Exception("错误的数据格式：{0}，请检查！error_info:{1}".format(case_except,e))


                check_value=self.obtain_quote_data(check_value, table_result)
                check_value=self.obtain_QuotoSituation_data(case_data["project"],case_data["QuotoSituation"], check_value)

                if isinstance(check_value,str) and "+" in check_value:
                    check_value = check_value.split("+")
                    handle_check_value = self.handle_string_obj(check_value[0])
                    for i in range(1,len(check_value)):
                        check_value[i] = self.handle_string_obj(check_value[i])
                        if type(handle_check_value)==type(check_value[i]):
                            if type(handle_check_value) ==str:
                                handle_check_value ="{0}{1}".format(handle_check_value,check_value[i])
                            elif type(handle_check_value) ==int:
                                handle_check_value=handle_check_value+check_value[i]
                            else:
                                raise Exception("{0}数据格式存在问题".format(check_value))
                    check_value = handle_check_value
                else:
                    check_value = self.handle_string_obj(check_value)

                if isinstance(check_value,str) and "&" in check_value:
                    check_value = check_value.split("&")

                except_info.append((obtain_obj_method, check_method, check_value))
        case_data["CaseExcept"]=except_info

        return table_result


if __name__ == '__main__':
    case = DataHandle().obtain_interface_cases("police_wiki","case")[0]
    print(case)
