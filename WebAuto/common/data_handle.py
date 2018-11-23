from WebAuto.common.json_handle import JsonHandle
from WebAuto.common.excel_data import Excel_Data
import glob
import  time

import os
import time,datetime

#p="common\\path_handle.py"即从项目一级目录开始
PATH=lambda P:os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),P))
dir_report_path=PATH("report\\")
email_config_path=PATH("data\\email_config.ini")
project_case_path=lambda p:PATH("project\\{0}\\case" .format(p))
project_data_path=lambda p:PATH("data\\{0}.xlsx" .format(p))
picture_path=PATH("picture\\" )

project_info_path=PATH("data\\web.json")
case_exeorder_path=PATH("data\\case_exeorder.xlsx")
driver_dir=PATH("drivers\\")

project_case_data_path=lambda p,c:PATH("project\\{0}\\data\\{1}" .format(p,c))


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

    def obtain_project_info(self,project):
        project_info = JsonHandle(project_info_path).jData[project]
        launch_info={}
        launch_info["driver"]=project_info["test_driver"]
        launch_info["driver_types"]=project_info["driver_types"]

        launch_info["test_version"]=project_info["test_version"]
        version_info=project_info[launch_info["test_version"]]
        launch_info["url"]=version_info[project_info["test_url"]]

        account_info={}
        account_info["username"]=version_info["username"]
        account_info["password"]=version_info["password"]
        return (launch_info,account_info)

    def timeData_handle(self,**kwargs):
        """
        时间参数处理
        :param kwargs:
        :return:
        """
        result_data={}
        if kwargs.get("end_time") and kwargs.get("start_time"):
            end_time = kwargs["end_time"]
            start_time = kwargs["start_time"]
        elif kwargs.get("end_time"):
            end_time = kwargs["end_time"]
            y, m, d = time.strptime(end_time, "%Y-%m-%d")[0:3]
            start_time = (datetime.datetime(y, m, d) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        elif kwargs.get("start_time"):
            start_time = kwargs["start_time"]
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
            start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        result_data["start_time"]=start_time
        result_data["end_time"] = end_time
        return result_data



if __name__ == '__main__':
    DataHandle().obtain_email_config()
