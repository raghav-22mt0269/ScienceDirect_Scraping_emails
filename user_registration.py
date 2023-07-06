
import sqlite3
import bcrypt

class Register_User:
    def __init__(self, db_name):
        self.db_name = db_name
        
    def createTable(self):
        

        con = sqlite3.connect(database=self.db_name)
        cursor = con.cursor()


        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        username TEXT,
        password TEXT);""")

        con.commit()
        con.close()


    """def RegisterUser(self):
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        print("#"*20)
        print("Registeration")
        print("#"*20)
        print("Enter your  Full Name:")
        name = input()
        print("Enter your preferred username:")
        username = input()
        print("Enter a password for your account:")
        password = input()
        encoded_password = password.encode("utf-8")
        hashed_pwd = bcrypt.hashpw(encoded_password, bcrypt.gensalt(12))
        
        if bcrypt.checkpw(encoded_password, hashed_pwd):
            print("Entered Password Matches with Hashed one")
            print("#"*20)
            print("Registration Successful")
            print("#"*20)
        else:
            print("Entered password is Wrong")
            
        cursor.execute("INSERT INTO users (name, username , password) VALUES (?, ?, ?)",
                    (name, username, hashed_pwd))
        
        conn.commit()
        conn.close()"""
        
    def login_user(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        print("#*#"*10)
        print("Welcome To Science Direct Scraper")
        print("#*#"*10)
        print("======= Login =======")
        print("Enter your username:")
        username = input()
        print("Enter your password:")
        pass_word = input().encode("utf-8")
        #rows = cursor.execute("SELECT name, username, password from users").fetchall()
        #print(rows)
        
        user_data = cursor.execute("SELECT username, password FROM users WHERE username = ?",(username,),).fetchone()
        #print(user_data)
        if user_data:
            if username == user_data[0]:
                if bcrypt.checkpw(pass_word, user_data[1]):
                    print("#*#"*10)
                    print("LogIn Successful...")
                    print("Scrapper is ready for use...")
                    print("#*#"*10)
                else:
                    print("#*#"*10)
                    print("Entered password is Wrong")
                    print("If you are not registered on this app, please contact the administration !")
                    #self.RegisterUser()
                    print("#*#"*10)
                    conn.commit()
                    conn.close()
                    exit()
        else:
            print("#*#"*10)
            print("Entered username does not exist")
            print("$$$$$$ please Contact your Administration! $$$$$$")
            #self.RegisterUser()
            print("#*#"*10)
            conn.commit()
            conn.close()
            exit()
        
        conn.commit()
        conn.close()
        
        