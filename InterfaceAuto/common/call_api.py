import requests
import json
import re
from InterfaceAuto.common.data_handle import PATH


class CallAPI:

    def handle_response(self,response):
        response_text = response.text
        try:
            r = json.loads(response_text)
        except Exception as e:
            print("Error:response_text={0}".format(response_text))
            raise Exception(response_text, e.args)
        return r


    def run(self,method, url, input=None,**kwargs):
        if method =="get":
            response=requests.get(url,params=input,**kwargs)
        elif method =="post":
            for key,value in input.items():
                if "data\\" in value:
                    filepath=PATH(value)
                    filename = "test" + re.search(r'\..*', filepath).group(0)
                    del input[key]
                    with open(filepath,"rb") as f:
                        files= {key: (filename,f)}
                        response = requests.post(url, data=input, files=files,**kwargs)
                        break
            else:
                response = requests.post(url, data=input)
        elif method =="put":
            response = requests.put(url, data=input,**kwargs)
        elif method =="delete":
            response = requests.delete(url,**kwargs)
        else:
            print("无法找到该方法：{0}".format(method))
            raise Exception(method)
        return self.handle_response(response)




