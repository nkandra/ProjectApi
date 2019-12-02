import string
import json
import sqlite3

class Password :
    def __init__(self):
        self.password_dict = {}
        self.syntax = {}
        try :
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute('select * from passwd')
            passwd_list = c.fetchall()
            conn.close()
        except :
            passwd_list = []

        for entry in passwd_list :
            self.password_dict[entry[0]] = [entry[1], entry[2]]
        print ("current db : {}".format(self.password_dict))

    def check_syntax(self, password):
        self.syntax['status'] = True
        self.syntax['log'] = "valid syntax, updating password"

        if len(password) < 4 :
            self.syntax['log'] = "Not a strong password"
            self.syntax['status'] = False
            return self.syntax
        for c in password:
            if not (c in string.ascii_letters or c in string.digits) :
                self.syntax['status'] = False
                self.syntax['log'] = "password contains invalid characters"
                return self.syntax
        return self.syntax

    def update_password(self,name, password):
        if name not in self.password_dict :
            self.password_dict[name] = [password, 'NULL']
            self.update_database()
            return True
        # elif len(self.password_dict[name])<2 :
        #     self.password_dict[name].append(password)
        #     self.update_database()
        #     return True
        elif password not in self.password_dict[name]:
            self.password_dict[name].pop(0)
            self.password_dict[name].append(password)
            self.update_database()
            return True
        else :
            return False

    def update_database(self):
        # self.password_data['password'] = [self.password_dict]
        # fh = open('password.json', 'w+')
        # with fh as f :
        #     json.dump(self.password_data, f)
        conn = sqlite3.connect('example.db')
        cc = conn.cursor()
        cc.execute("select count(name) from sqlite_master where type = 'table' and name = 'passwd'")
        #import  pdb; pdb.set_trace()
        print ( "next db {}".format(self.password_dict))
        if cc.fetchall()[0][0] == 1 :
            for key, value in self.password_dict.items() :
                query = "insert into passwd values ('{}', '{}', '{}')".format(str(key), str(value[0]), str(value[1]))
                #import pdb;pdb.set_trace()
                cc.execute(query)
        else :
            query = "create table passwd (name text, pass1 text, pass2 text)"
            cc.execute(query)
            for key, value in self.password_dict.items() :
                query = "insert into passwd values ('{}', '{}', '{}')".format(str(key), str(value[0]), str(value[1]))
                cc.execute(query)
        conn.commit()
        conn.close()


if __name__ == '__main__' :
    p = Password()
    n = input("Enter your username : ")
    pa = input("Enter password : ")
    pa_status = p.check_syntax(pa)
    if pa_status['status'] :
        if p.update_password(n, pa) :
            print ("password update successful ")
        else :
            print("This password already is already used")
    else :
        print("Not a vaild syntax, update failed")



