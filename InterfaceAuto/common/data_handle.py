from InterfaceAuto.common.json_handle import JsonHandle
from InterfaceAuto.common.excel_data import Excel_Data
import os
import glob
import  time

#p="common\\path_handle.py"即从项目一级目录开始
PATH=lambda P:os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),P))
dir_report_path=PATH("report\\")
email_config_path=PATH("data\\email_config.ini")
project_case_path=lambda p:PATH("server\\{0}".format(p))


project_case_data=lambda p,m:Excel_Data(PATH("data\\{0}.xlsx".format(p)),m)
prefix_url_path=PATH("data\\interface_info.json")
case_exeorder_path=PATH("data\\case_exeorder.xlsx")


class DataHandle:
    def obtain_email_config(self):
        email_config_info={}
        suffix_config_file=os.path.splitext(email_config_path)[1]
        if suffix_config_file==".ini":
            import configparser
            email_config=configparser.ConfigParser()
            email_config.read(email_config_path,encoding="utf-8")
            email_config_info["server"]=email_config.get("email","server")
            email_config_info["sender"] = email_config.get("email", "sender")
            email_config_info["password"] = email_config.get("email", "password")
            email_config_info["receiver"] = eval(email_config.get("email", "receiver"))
            email_config_info["title"] = email_config.get("email", "title")
            email_config_info["message"] = email_config.get("email", "message")
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
        prefix_url_data=JsonHandle(prefix_url_path).jData
        if prefix_url_data.get(project):
            project_info =prefix_url_data[project]
            base_url=project_info.get("base_url")
            base_except=project_info.get("base_except")
            if project_info.get(module):
                module_info=project_info[module]
                module_url = module_info.get("module_url")
                module_except=module_info.get("module_except")
                if module_info.get(interface):
                    interface_info=module_info[interface]

                    interface_url=base_url+module_url+interface
                    interface_info["url"]= interface_url

                    interface_except=interface_info.get("interface_except") or []
                    interface_except.extend(module_except)
                    interface_except.extend(base_except)
                    interface_info["interface_except"]=interface_except
                    return interface_info
                else:
                    print("{0}该模块下未找到接口：{1}".format(module, interface))
                    raise Exception("{0}该模块下未找到接口：{1}".format(module, interface))
            else:
                print("{0}该项目下未找到模块：{1}".format(project,module))
                raise Exception("{0}该项目下未找到模块：{1}".format(project,module))
        else:
            print("未找到项目：{0}".format(project))
            raise Exception("未找到项目：{0}".format(project))

    # 解析并获取excel文件里面的某个接口全部测试用例
    def obtain_interface_cases(self,project,module,interface):
        case_list=[]
        data_list=project_case_data(project,module).data

        for data in data_list:
            if data["TestInterface"] ==interface :
                interface_info=self.obtain_interface_info(project,module,interface)
                data.update(interface_info)
                case_list.append(data)
        return case_list




if __name__ == '__main__':
    case = DataHandle().obtain_interface_cases("police_wiki","case","causeRecommend")[0]
    print(case)
