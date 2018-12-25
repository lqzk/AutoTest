import requests
import json
import re


class CallAPI:

    def handle_response(self,response):
        handle_response={}
        try:
            handle_response["res"] = json.loads(response.text)
        except Exception as e:
            handle_response["res"]=response.content

        handle_response["Res_headers"]=dict(response.headers)
        handle_response["cookies"]=response.cookies
        handle_response["res_time"]=response.elapsed.total_seconds()
        handle_response["status_code"]=response.status_code

        return handle_response



    def run(self,method, url, input=None,headers=None,files=None):
        if method =="get":
            response=requests.get(url,params=input,headers=headers)
        elif method =="post":
            response = requests.post(url, data=input,headers=headers,files=files)
        elif method =="put":
            response = requests.put(url, data=input)
        elif method =="delete":
            response = requests.delete(url)
        else:
            print("无法找到该方法：{0}".format(method))
            raise Exception(method)
        return self.handle_response(response)




