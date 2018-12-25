import requests, json
from InterfaceAuto.common.excel_data import Excel_Data

excel_result = Excel_Data("F:\\Intelligent_mediation\\InterfaceAuto\\data\\南京市违法代码结果.xlsx", "Sheet1")

# search_excel=Excel_Data("F:\\Intelligent_mediation\\InterfaceAuto\\data\\违法代码表.xlsx","Sheet0")
search_excel = Excel_Data("F:\\Intelligent_mediation\\InterfaceAuto\\data\\南京市违法代码.xlsx", "Sheet1")
search_data = search_excel.data

# for each_data in data:
#     print(each_data)
#     excel_result.data=each_data

error_code = []

for each_search_data in search_data:

    each_search_data["Result"] = "False"
    res = requests.get("http://61.155.9.140:8282/traffic_illegal_action/query/list",
                       params={"code": int(each_search_data["code"])})
    res_test = json.loads(res.text)
    if res_test["data"]["data"] != []:
        data = res_test["data"]["data"][0]
        print(each_search_data)
        print(data)
        if each_search_data["name"] != data.get("name"):
            error_msg = "name_error:{0}".format(data.get("name"))
        elif each_search_data["illegalGist"] != data.get("illegalGist"):
            error_msg = "illegalGist_error:{0}".format(data.get("illegalGist"))
        elif each_search_data["publishGist"] != data.get("publishGist"):
            error_msg = "publishGist_error:{0}".format(data.get("publishGist"))
        # elif each_search_data["score"] not in [data.get("score"),"",None]:
        #     error_msg = "publishGist_error:{0}".format(data.get("publishGist"))
        # elif each_search_data["otherPublish"] not in [data.get("otherPublish"), "", None]:
        #     error_msg = "otherPublish_error:{0}".format(data.get("otherPublish"))
        # elif each_search_data["otherMeasure"] not in [data.get("otherMeasure"), "", None]:
        #     error_msg = "otherMeasure_error:{0}".format(data.get("otherMeasure"))
        elif str(each_search_data["fine"]) not in [data.get("fine"), "", None, "{0}.0".format(data.get("fine"))]:
            error_msg = "fine_error:{0}".format(data.get("fine"))
        else:
            error_msg = ""
            each_search_data["Result"] = "True"
    else:
        error_msg = "无此数据"

    each_search_data["error_msg"] = error_msg

    if error_msg != "":
        error_code.append(int(each_search_data["code"]))

    print(error_msg)
    print(each_search_data["Result"])
    print("\n\n\n")
    excel_result.data = each_search_data

print(error_code)









