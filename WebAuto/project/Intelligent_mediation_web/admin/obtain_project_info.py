from InterfaceAuto.common.json_handle import JmespathExtractor
JExtractor = JmespathExtractor()

def project_info(project_data,key):
    test_environment = project_data["test_environment"]
    if key == "AdminURL":
        obtain_info = project_data[key][test_environment]
    else:
        obtain_info = JExtractor.extract(key, project_data)
    return obtain_info