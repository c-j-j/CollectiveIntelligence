import sqlite3

class database:
    def __init__(self,dbname):
        self.dbConnection = sqlite3.connect(dbname)

    def close(self):
        self.dbConnection.close()

    def dbcommit(self):
        self.dbConnection.commit()

    def execute(self,statement):
        self.dbConnection.execute(statement)