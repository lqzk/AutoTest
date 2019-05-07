from InterfaceAuto.common.run_suite import RunSuite
from InterfaceAuto.common.treadpool import ThreadPool

if __name__ == '__main__':

    # my_pool=ThreadPool(RunSuite().run,3,["Risk_assess"])
    # my_pool.pool()

    # all_project_list=["Intelligent_mediation","Intelligent_mediation_web","Risk_assess","Intelligent_judgement",'File_handle_service']
    # project_list=["Intelligent_mediation","Risk_assess"]
    # for project in project_list:
    #     print("S")
    #     RunSuite().run(project)
    #     print("E")

    # project_list = ["Risk_assess"]
    # [RunSuite().run(project) for project in project_list]

    RunSuite().run("Intelligent_mediation")






