from InterfaceAuto.common.run_suite import RunSuite


if __name__ == '__main__':
    project_name = "Intelligent_mediation"
    RunSuite().run(project_name,send_email=True)
    #
    # import time
    # time.sleep(2)

    # project_name = "Intelligent_mediation_web"
    # RunSuite().run(project_name,send_email=True)






