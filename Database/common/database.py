from Database.common.system import System

class DataBase(System):
    def __init__(self,database=None):
        if database:
            self.cnn=database.cnn
            self.cursor=self.cnn.cursor()
        else:
            super(DataBase,self).__init__()

    def execute_cursor(self, query, args):
        self.cursor.execute(query, args)

    def executemany_cursor(self, query, args):
        self.cursor.executemany(query, args)

    def nextset_cursor(self):
        self.cursor.nextset()

    def fetch(self,row):
        if row=="all":
            self.cursor.fetchall()
        elif row==1:
            self.cursor.fetchone()
        else:
            self.cursor.fetchmany(row)



    def rollback(self):
        import traceback
        traceback.print_exc()
        self.cnn.rollback()

    def close(self):
        self.cursor.close()
        self.cnn.close()

    def select(self):
        pass
