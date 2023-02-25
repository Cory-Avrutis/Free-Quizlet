# This file should act as an API for intereactions with
# the database. Functions should be made clear and concise
# for CRUD operations and adhere to role-based acess constraints.

# User --> Read/Create/Update/Delete OWN Sets; Read OTHER sets
# Mod  --> Read/Create/Update/Delete OWN/OTHER Sets; Read OTHER accounts
# Admn --> Read/Create/Update/Delete OWN/OTHER Sets; Read/Update OTHER accounts

from pymongo import MongoClient
import bcrypt

conn_str = "mongodb+srv://quizuser:quizpassword@quizlet.gnboxhj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str)


db = client["quizlet"]
users = db["users"]


# inserts a new user record into a collection
def insert_new_user(usr, pwd, email):
    rec = {
            "username" : usr,
            "password" : pwd,
            "privs"    : "user",
            "email"    : email
          }
    users.insert_one(rec)

# returns True if email is unique in db
def email_exists(email):
    if users.find_one({"email" : email}):
        return True
    return False

# returns True if username is unique in db
def username_exists(usr):
    if users.find_one({"username" : usr}):
        return True
    return False

# returns encrypted password for usr from db
def get_password(usr):
    if users.find_one({"username" : usr}):
        user = users.find_one({"username" : usr})
        return user["password"]


# To create a collection in db
# newColl = db["new_coll_name"]

# To insert a record in a collection
'''
root = 	{	
		"username" : "root",
        "password" : "root",
        "privs"    : "admin",
        "email"    : "cavrutis@fsu.edu"
	 	}

users.insert_one(root)
'''

# To update a field in a record
filt = {"username" : "root"}
update = {"$set" : {"password" : bcrypt.hashpw("root".encode("utf-8"), bcrypt.gensalt())}}
users.update_one(filt, update)

print("Success")







