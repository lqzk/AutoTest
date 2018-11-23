import unittest
import time
from WebAuto.common.data_handle import DataHandle,dir_report_path,project_case_path
from WebAuto.common.email import Email


class RunSuite:
    def create_suite(self,project_name,ordered=False,pattern='test*.py'):
        # 导入该项目下全部测试用例模块
        import_statement = DataHandle().obtain_import_cases_statement(project_name)
        exec(import_statement)


        if not ordered:
            suite=unittest.defaultTestLoader.discover(project_case_path(project_name),pattern=pattern,top_level_dir=project_case_path(project_name))
        else:
            test_case_list = DataHandle().obtain_case_exe_order(project_name)
            suite=unittest.TestSuite()
            for case in test_case_list:
                suite.addTest(eval(case))
        return suite

    def run(self,project_name,pattern='test*.py',ordered=False,html_report=True,send_email=False):


        #创建测试用例
        suite=self.create_suite(project_name=project_name,ordered=ordered,pattern=pattern)

        #生成测试报告并运行测试用例
        if not html_report:
            runner=unittest.TextTestRunner()
            runner.run(suite)
        else:
            from AppAuto.common.HTMLTestRunner_PY3 import HTMLTestRunner
            now=time.strftime("%y-%m-%d-%H-%M-%S",time.localtime(time.time()))
            report_path=dir_report_path+now+".html"
            print(report_path)
            with open(report_path,"wb") as f:
                runner=HTMLTestRunner(stream=f,verbosity=2,title=u'自动化测试报告',
                            description=u'用例执行情况')
                runner.run(suite)

            # 是否发邮件
            if send_email:
                Email().send_email(DataHandle().obtain_email_config())
















