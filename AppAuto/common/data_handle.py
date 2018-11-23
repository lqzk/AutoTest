from AppAuto.common.json_handle import JsonHandle
from AppAuto.common.excel_data import Excel_Data
import glob
import  time

import os
#p="common\\path_handle.py"即从项目一级目录开始
PATH=lambda P:os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),P))
dir_report_path=PATH("report\\")
email_config_path=PATH("data\\email_config.ini")
project_case_path=lambda p:PATH("project\\{0}\\case".format(p))

all_mobile_info_path=PATH("data\\all_mobile_info.json")
all_account_info_path=PATH("data\\all_account_info.json")
setting_path=PATH("data\\app.json")
case_exeorder_path=PATH("data\\case_exeorder.xlsx")
project_data=lambda p:JsonHandle(setting_path).jData[p]


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

    def obtain_lanuch_parm(self,project):
        desired_caps={}
        desired_caps['noReset'] = 'True'
        all_mobile_info_data = JsonHandle(all_mobile_info_path).jData
        usePhone = project_data(project)["Phone"]
        UseApp = project_data(project)["App"]
        usePhoneParm =all_mobile_info_data["Phone"].get(usePhone)
        useAppParm   =all_mobile_info_data["App"].get(UseApp)

        if usePhoneParm:
            desired_caps.update(usePhoneParm)
            if useAppParm:
                desired_caps.update(useAppParm)
                print("[lanuch]成功获取登录参数:\n  PhoneName:{0}\n  AppName:{1}".format(
                    usePhoneParm, useAppParm))
            else:
                print("[lanuch]can't find app in mobile_config file:{0}".format(UseApp))
        else:
            print("[lanuch]can't find phone in mobile_config file:{0}".format(usePhone))
        return  desired_caps
    
    def obtain_login_account(self,project):
        login_account=project_data(project)["Login_account"]
        all_account_info_data = JsonHandle(all_account_info_path).jData
        account=all_account_info_data[login_account]
        print("[login]成功获取登录账户:\n  account:{0}\n  password:{1}".format(account["account"],account["password"]))
        return account





if __name__ == '__main__':
    DataHandle().obtain_email_config()
