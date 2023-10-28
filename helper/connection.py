# from api import process_file
import mysql.connector as mysql
from dotenv import load_dotenv
load_dotenv()
from os import environ
class DbConnection:
    def __init__(self,to_close=True):
        try:
            self.con = mysql.connect(host=environ.get("DB_HOST"),
                                    database=environ.get("DATABASE_NAME"),
                                    user=environ.get("DB_USER"),
                                    password=environ.get("DB_USER_PASSWORD"))
            self.cursor= self.con.cursor()
            self.to_close=to_close
        except:
            raise Exception("Unable to connect")
        
    def insert(self,query):
        try:
            self.cursor.execute(query)      
            self.con.commit()
            id = self.cursor.lastrowid
            resp=id
        except Exception as e:
            resp=""
            print(str(e))
        finally:
            if self.to_close:
                self.closeConnection()
            return resp


    def get(self, condition_1="", condition_2="", table_name="",order_by = ""):
        try:
            query= f"""SELECT {condition_1} FROM {table_name}"""
            if condition_2:
                query+=f" WHERE {condition_2}"
            if order_by:
                query+=f" ORDER BY {order_by}"
            self.cursor.execute(query)
            column_names = [col[0] for col in self.cursor.description]
            data_dict = [dict(zip(column_names, row)) for row in self.cursor.fetchall()]    
            resp=data_dict   
        except Exception as e:
            resp=[]
        finally:
            if self.to_close:
                self.closeConnection()
            return resp

    def update(self,query):
        try:
            self.cursor.execute(query)  
            self.con.commit()
            resp=True
        except Exception as e:
            resp=False
        finally:
            if self.to_close:
                self.closeConnection()
            return resp

    def closeConnection(self):
        self.cursor.close()