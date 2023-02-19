# This file should act as an API for intereactions with
# the database. Functions should be made clear and concise
# for CRUD operations and adhere to role-based acess constraints.

# User --> Create/Update/Delete OWN Sets; Read OTHER sets
# Mod  --> Read/Create/Update/Delete OWN/OTHER Sets; Read OTHER accounts
# Admn --> Read/Create/Update/Delete OWN/OTHER Sets; Read/Update OTHER accounts

from pymongo import MongoClient

conn_str = "mongodb+srv://pygroup:rcagroup@project.uxruw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str)


# Returns the database holding login info
def get_logindb():
	return client["logindb"]


#logindb = get_logindb()

# To create a collection in logindb
#logins = logindb["logins"]

# To insert a record in a collection
#me = 	{	
#		"user" : "pass"
#	 	}

#logins.insert_one(me)
print("Success")



