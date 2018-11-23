import pymysql
from Database.common.data_handle import DataHandle

class System(object):
    def __init__(self):
        self.cnn=None
        self.cursor=None

    def connect(self):
        self.cnn=pymysql.connect(DataHandle().obtain_connect_parm())
        self.cursor = self.cnn.cursor()
        return self

