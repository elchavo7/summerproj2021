import sqlite3

import pickle
    # https://docs.python.org/2/library/sqlite3.html
    # https://www.youtube.com/watch?v=U7nfe4adDw8


__author__ = 'user'


class Computer(object):
    def __init__(self,serial_num,brand_name,gpu,ram,storage, is_mobile):
        self.serial_num = serial_num
        self.brand_name = brand_name
        self.gpu = gpu
        self.ram = ram
        self.storage = storage
        self.is_mobile = is_mobile

    def __str__(self):
        return "user:"+self.serial_num+":"+str(self.brand_name)+":"+str(self.gpu)+":" + \
                      self.ram+":"+self.storage+":"+str(self.is_mobile)


class Apps(object):
    def __init__(self,app_id,app_size,app_name, app_location):
        self.app_id=app_id
        self.app_size=app_size
        self.app_name=app_name
        self.app_location=app_location


class ComputerAppORM():
    def __init__(self):
        self.conn = None  # will store the DB connection
        self.cursor = None   # will store the DB connection cursor


    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect('ComputerApp2.db')
        self.current = self.conn.cursor()

    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    #All read SQL

    def GetComputer(self,serial):
        self.open_DB()

        sql = f"SELECT * FROM Computer WHERE serial_num = '{serial}'"
        self.current.execute(sql)
        self.conn.commit()
        comp = self.current.fetchall()
        self.close_DB()
        return comp
    
    def GetAccounts(self):
        pass

    def GetComputers(self, data):
        self.open_DB()
        print(type(data))
        usrs=[]
        if data == "1":
            sql = "SELECT * FROM Computer"
        elif data == "2":
            sql = "SELECT * FROM Computer WHERE is_mobile = 1"
        elif data == "3":
            sql = "SELECT * FROM Computer WHERE is_mobile = 0"

            print("here")
        else:
            return []
        res = self.current.execute(sql)
        self.conn.commit()
        usrs = self.current.fetchall()
        #print(usrs)
        self.close_DB()
        return usrs


    def get_user_balance(self,username):
        self.open_DB()

        sql="SELECT a.Balance FROM Accounts a , Users b WHERE a.Accountid=b.Accountid and b.Username='"+username+"'"
        res = self.current.execute(sql)
        for ans in res:
            balance =  ans[0]
        self.close_DB()
        return balance


    #__________________________________________________________________________________________________________________
    #__________________________________________________________________________________________________________________
    #______end of read start write ____________________________________________________________________________________
    #__________________________________________________________________________________________________________________
    #__________________________________________________________________________________________________________________
    #__________________________________________________________________________________________________________________




    #All write SQL


    def withdraw_by_username(self,amount,username):
        """
        return true for success and false if failed
        """
        pass
        

    def deposit_by_username(self,amount,username):
         pass




    def insert_new_user(self,username,password,firstname,lastname,address,phone,email,acid):
         pass


    def insert_computer(self,serial_num,brand_name,gpu,ram,storage,bool_mobile):
        self.open_DB()
        print(bool_mobile +":bool")
        sql = f"INSERT INTO Computer(serial_num,brand_name,gpu,ram,storage,is_mobile)" \
              f"VALUES ('{str(serial_num)}','{brand_name}','{gpu}','{ram}','{storage}','{bool_mobile}');" \

        res = self.current.execute(sql)
        self.commit()
        self.close_DB()
        return res

    def update_computer(self, change):
        self.open_DB()
        sql = f"UPDATE Computer SET '{change.split('|')[0]}' = '{change.split('|')[1]}' WHERE serial_num = '{change.split('|')[2]}'"
        res = self.current.execute(sql)
        self.commit()
        self.close_DB()
        return res

    def update_account(self,account):
        pass


    def delete_computer(self,serial):

        self.open_DB()

        sql = "SELECT COUNT(*) FROM Computer"
        res = self.current.execute(sql)
        self.conn.commit()
        row_num = self.current.fetchall()[0][0]
        sql = f"DELETE FROM Computer WHERE serial_num='{serial}';"
        self.current.execute(sql)
        self.conn.commit()

        sql = "SELECT COUNT(*) FROM Computer"
        res = self.current.execute(sql)
        self.conn.commit()
        if self.current.fetchall()[0][0] < row_num:
            return True
        else:
            return False


    def delete_account(self,accountID):
        pass


def main_test():
    user1= Computer("Yos","12345","yossi","zahav","kefar saba","123123123","1111",1,'11')

    db = ComputerAppORM()
    db.delete_user(user1.user_name)
    users = db.get_users()
    for u in users :
        print (u)


if __name__ == "__main__":
    main_test()


