import json

import jmespath
import json


class JmespathExtractor(object):
    """
        用JMESPath实现的抽取器，对于json格式数据实现简单方式的抽取。
    """
    def extract(self,quary=None,body=None):
        try:
            # return jmespath.search(quary, json.loads(body))
            return jmespath.search(quary, body)
        except Exception as e:
            raise ValueError("Invalid quary :"+quary+":"+str(e))


class JsonHandle:
    def __init__(self,jsonfile_path):
        self.jsonfile_path=jsonfile_path

    @property
    def jData(self):
        try:
            try:
                with open(self.jsonfile_path, "r", encoding="gbk") as f: return json.load(f)
            except Exception as e:
                raise Exception(str(e))
        except:
            try:
                with open(self.jsonfile_path,"r",encoding="utf-8") as f: return json.load(f)
            except Exception as e:
                raise Exception(str(e))


    @jData.setter
    def jData(self,dicdata):
        try:
            try:
                with open(self.jsonfile_path, "w+", encoding="gbk") as f:
                    json.dump(dicdata,f, ensure_ascii=False)
            except Exception as e:
                raise Exception(str(e))
        except:
            try:
                with open(self.jsonfile_path, "w+", encoding="utf-8") as f:
                    json.dump(dicdata, f, ensure_ascii=False)
            except Exception as e:
                raise Exception(str(e))


if __name__ == '__main__':
    data=JsonHandle("F://Function//config//mobile_config.json").jData
    print(data)






