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
card_sets = db["card_sets"]


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
    return None

def set_exists(user:str, title:str):
    if card_sets.find_one({'User' : user, 'Title' : title}):
        return True
    return False

# inserts a new record into card_sets collection    
def insert_new_card_set(cards : dict, title : str, usr : str,):
    rec = {
        "Cards" : cards,    
        "Title" : title,
        "User" : usr
    }
    card_sets.insert_one(rec)

# return all card_sets based on a privilege level
def get_sets_by_privs(priv:str):
    if priv == 'admin':
        return [x for x in card_sets.find()]
    elif priv == 'mod':
        return [x for x in card_sets.find() if users.find_one({"username" : x['User']})['privs'] != 'admin']
    else:
        return [x for x in card_sets.find() if users.find_one({"username" : x['User']})['privs'] == 'user']
            
# return sets for User and Title
def get_set_by_user_title(usr:str, title:str):
    return [x for x in card_sets.find({'User' : usr}) \
              if x['Title'] == title][0]

# return all card_sets based on a username
def get_sets_by_user(usr:str):
    return card_sets.find({'User' : usr})

# search sets by Title
def get_sets_by_title(title:str):
    return card_sets.find({'Title' : title})


# update set with given Title and User
def update_title(user:str, old_title:str, new_title:str):
    card_sets.update_one( 
        {"User": user, "Title": old_title}, #query to extract which title
        {"$set": {"Title": new_title}}      #query to update the title
    ) 


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







