import time
import unittest
import re
from InterfaceAuto.common.data_handle import DataHandle, dir_report_path, project_case_path,email_list
from InterfaceAuto.common.email import Email


class RunSuite:
    def create_suite(self,project_name,ordered=False,pattern='test*.py'):
        # 导入该项目下全部测试用例模块
        # import_statement = DataHandle().obtain_import_cases_statement(project_name)
        # exec(import_statement)
        # suite=unittest.defaultTestLoader.discover(project_case_path(project_name),pattern=pattern,top_level_dir=project_case_path(project_name))

        if not ordered:
            suite = unittest.TestSuite()
            discover = unittest.defaultTestLoader.discover(project_case_path(project_name), pattern=pattern,
                                                        top_level_dir=project_case_path(project_name))
            suite.addTest(discover)

        else:
            test_case_list = DataHandle().obtain_case_exe_order(project_name)
            suite=unittest.TestSuite()
            for case in test_case_list:
                suite.addTest(eval(case))
        return suite

    def run(self,project_name,pattern='test*.py',ordered=False,html_report=True,send_email=False,error=True):

        #创建测试用例
        suite=self.create_suite(project_name=project_name,ordered=ordered,pattern=pattern)

        #生成测试报告并运行测试用例
        if not html_report:
            runner=unittest.TextTestRunner()
            runner.run(suite)
        else:
            from InterfaceAuto.common.HTMLTestRunner_PY3 import HTMLTestRunner

            now=time.strftime("%y-%m-%d-%H-%M-%S",time.localtime(time.time()))
            report_path=dir_report_path+now+".html"
            print(report_path)
            with open(report_path,"wb") as f:
                runner=HTMLTestRunner(stream=f,verbosity=2,title=u'{0}自动化测试报告'.format(project_name),
                            description=u'用例执行情况')
                result=runner.run(suite)


            # 是否发邮件
            if send_email:
                email_config = DataHandle().obtain_email_config(project_name)

                #当存在错误时，发送给制定负责人
                if error==True:
                    send_email_list = []
                    for error in result.errors:
                        if re.search(r"leader\_(.*?)$", error[0]._testMethodName):
                            error_leaders_name = re.search(r"leader\_(.*?)$", error[0]._testMethodName).group(1)
                            error_leaders_list = error_leaders_name.split("_")
                            send_email_list.extend(error_leaders_list)
                    send_email_list=list(set(send_email_list))
                    if not send_email_list==[]:
                        for each_leader in send_email_list:
                            email_config["receiver"].append(email_list[each_leader])

                if not email_config["receiver"] == []:
                    Email().send_email(email_config)










