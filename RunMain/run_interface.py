from InterfaceAuto.common.run_suite import RunSuite
import time

if __name__ == '__main__':
    project_name = "police_wiki"
    RunSuite().run(project_name)

    time.sleep(1)

    project_name = "weather"
    RunSuite().run(project_name)


