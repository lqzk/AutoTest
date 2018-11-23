import requests
import json


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
            response = requests.post(url,data=input, **kwargs)
        elif method =="put":
            response = requests.put(url, data=input,**kwargs)
        elif method =="delete":
            response = requests.delete(url,**kwargs)
        else:
            print("无法找到该方法：{0}".format(method))
            raise Exception(method)
        return self.handle_response(response)




