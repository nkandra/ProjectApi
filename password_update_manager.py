import string
import json

class Password :
    def __init__(self):
        try :
            fh = open('password.json', 'r')
            with fh as json_data :
                self.password_data = json.load(json_data)
        except :
            self.password_data = {}

        if 'password' not in self.password_data :
            self.password_data['password'] = [{}]
        self.syntax = {}
        self.password_dict = self.password_data['password'][0]

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
            self.password_dict[name] = [password]
            self.update_database()
            return True
        elif len(self.password_dict[name])<2 :
            self.password_dict[name].append(password)
            self.update_database()
            return True
        elif password not in self.password_dict[name]:
            self.password_dict[name].pop(0)
            self.password_dict[name].append(password)
            self.update_database()
            return True
        else :
            return False

    def update_database(self):
        self.password_data['password'] = [self.password_dict]
        fh = open('password.json', 'w+')
        with fh as f :
            json.dump(self.password_data, f)

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



