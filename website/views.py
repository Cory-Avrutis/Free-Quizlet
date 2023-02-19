from flask import Blueprint, render_template

# Define a blueprint called "views" for webpage viewing
views = Blueprint("views", __name__)

'''
Redirect to the homepage or index.html 
'''
@views.route("/")
def home():
	return render_template("home.html")

	
