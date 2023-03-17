# This file should act as an API for intereactions with
# the database. Functions should be made clear and concise
# for CRUD operations and adhere to role-based acess constraints.

# User --> Read/Create/Update/Delete OWN Sets; Read OTHER sets
# Mod  --> Read/Create/Update/Delete OWN/OTHER Sets; Read OTHER accounts
# Admn --> Read/Create/Update/Delete OWN/OTHER Sets; Read/Update OTHER accounts

from pymongo import MongoClient
import bcrypt
import certifi

conn_str = "mongodb+srv://quizuser:quizpassword@quizlet.gnboxhj.mongodb.net/quizlet?retryWrites=true&w=majority"
client = MongoClient(conn_str, tlsCAFile=certifi.where())


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

# return username given the email
def get_username(email):
    usr = users.find_one({"email" : email})
    return usr["username"]

# returns encrypted password for usr from db
def get_password(usr):
    if users.find_one({"username" : usr}):
        user = users.find_one({"username" : usr})
        return user["password"]
    

    
sets = db["sets"]
def insert_new_cards(cards : dict, title : str, usr : str,):
    rec = {
        "Cards" : cards,    #this prob won't work right because cards is itself a dictionary. update: it did work !
        "Title" : title,
        "User" : usr
    }
    users.insert_one(rec)
    

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
'''
filt = {"username" : "root"}
update = {"$set" : {"password" : bcrypt.hashpw("root".encode("utf-8"), bcrypt.gensalt())}}
users.update_one(filt, update)
'''
#username_exists("root")
#print("Success")







