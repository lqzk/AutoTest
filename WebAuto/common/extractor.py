import jmespath
import json


class JmespathExtractor(object):
    """
        用JMESPath实现的抽取器，对于json格式数据实现简单方式的抽取。
    """
    def extract(self,quary=None,body=None):
        try:
            return jmespath.search(quary, json.loads(body))
        except Exception as e:
            raise ValueError("Invalid quary :"+quary+":"+str(e))



