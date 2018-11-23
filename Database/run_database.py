from Database.common.database import DataBase
import unittest


class run(unittest.TestCase):
    def test(self):
        self.database = DataBase().connect()
        try:
            #支持语句部分
            self.database.execute_cursor()



        except:
            self.database.rollback()
        finally:
            self.database.close()



