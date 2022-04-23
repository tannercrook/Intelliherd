import dateutil.parser
import hashlib, uuid
from models.DBase import connection

class User(object):

    def __init__(self):
        self.userID = 0
        self.user_id = 0
        self.email = ""
        self.last_name = ""
        self.first_name = ""
        self.password = ""
        self.salt = ""
        self.created_by = 0
        self.date_created = ""
        self.modified_by = 0
        self.date_modified = ""
        self.force_password_change = 0
        self.login_fail_count = 0
        self.admin = 0

        # Flask-login Components
        self.is_authenticated=False
        self.is_active=False
        self.is_anonymous=False 

        # AdminLTE Components
        self.full_name = ""
        self.avatar = "#"
        self.created_at = dateutil.parser.parse("November 12, 2019")

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password

    def get_id(self):
        return self.user_id

    def makeUserAuth(self):
        try:
            c, conn = connection()
            c.execute("SELECT * FROM system_user WHERE email='{}';".format(self.email))
            result_set = c.fetchall()
            conn.close()

            # Check the results
            if(len(result_set) == 1):
                for row in result_set:
                    self.userID = row['user_id']
                    self.email = row['email']
                    self.firstName = row['first_name']
                    self.lastName = row['last_name']
                    self.user_id = chr(row['user_id'])
                    realPassword = row['password']
                    self.salt = row['salt']
                    self.date_created = row['date_created']
                    self.created_by = row['created_by']
                    self.date_modified = row['date_modified']
                    self.modified_by = row['modified_by']
                    self.force_password_change = row['force_password_change']
                    self.login_fail_count = row['login_fail_count']
                    self.admin = row['admin']
                    hashedPassword = hashlib.sha512(self.password+self.salt.encode('utf-8')).hexdigest()
                    if hashedPassword == realPassword:
                        self.is_authenticated = True
                        self.is_anonymous = True
                        self.is_active = True
                        return True
                    else:
                        return False
            else:
                # Something isn't right
                return False

        except Exception as e:
            return(e)

    def get(self, user_id):
        try:
            c, conn = connection()
            c.execute("SELECT * FROM system_user WHERE user_id={};".format(int(ord(user_id))))
            result_set = c.fetchall()
            conn.close()

            # Check the results
            if(len(result_set) == 1):
                for row in result_set:
                    self.userID = row['user_id']
                    self.email = row['email']
                    self.firstName = row['first_name']
                    self.lastName = row['last_name']
                    self.user_id = chr(row['user_id'])
                    self.salt = row['salt']
                    self.date_created = row['date_created']
                    self.created_by = row['created_by']
                    self.date_modified = row['date_modified']
                    self.modified_by = row['modified_by']
                    self.force_password_change = row['force_password_change']
                    self.login_fail_count = row['login_fail_count']
                    self.admin = row['admin']
                    self.is_authenticated = True
                    self.is_anonymous = True
                    self.is_active = True
                    return self
            else:
                # Something isn't right
                return None

        except Exception as e:
            return(self)

    def createUser(self):
        try:
            c, conn = connection()
            c.execute("INSERT INTO system_user (email,last_name,first_name,password,salt) VALUES (%s,%s,%s,%s,%s);",(self.email,self.lastName,self.firstName,self.password,self.salt))
            conn.commit()
            conn.close()
            return "<p> Create Successfully </p>"
        except Exception as e:
            return str(e)


    def fetch(self, user_id):
        try:
            c, conn = connection()
            c.execute("SELECT * FROM system_user WHERE user_id={};".format(int(ord(user_id))))
            result_set = c.fetchall()
            conn.close()

            # Check the results
            if(len(result_set) == 1):
                for row in result_set:
                    self.userID = row['user_id']
                    self.email = row['email']
                    self.firstName = row['first_name']
                    self.lastName = row['last_name']
                    self.user_id = chr(row['user_id'])
                    self.salt = row['salt']
                    self.date_created = row['date_created']
                    self.created_by = row['created_by']
                    self.date_modified = row['date_modified']
                    self.modified_by = row['modified_by']
                    self.force_password_change = row['force_password_change']
                    self.login_fail_count = row['login_fail_count']
                    self.admin = row['admin']
                    return self
            else:
                # Something isn't right
                return None

        except Exception as e:
            return(self)


    def update(self):
        try:
            c, conn = connection()
            c.execute("UPDATE system_user SET email=%s, first_name=%s, last_name=%s WHERE user_id = %s;",(self.email,self.firstName,self.lastName,self.userID))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

