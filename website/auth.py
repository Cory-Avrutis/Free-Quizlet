from flask import url_for, flash, Blueprint, render_template, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from .database import *
from .models import User
import bcrypt

# Define the "auth" blueprint to handle authorization and security
auth = Blueprint("auth", __name__)

'''
Redirect to the login page
    support GET and POST reguests
'''
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
       
        # Check username exists
        if not username_exists(username):         
            flash("Username does not exist", category="error")
        # Check password is correct
        elif not bcrypt.checkpw(password.encode("utf-8"), get_password(username)):
            flash("Password is incorrect", category="error")
        else:
            flash("Login Successful", category="success")
            user = User(username)
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    
    return render_template("login.html", user=current_user)

'''
Redirect to the logout page
'''
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

'''
Redirect to the sign-up page
    Supports GET and POST requests
'''
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    # Post Request --> Usr requesting to sign up
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password2')
    
        # Validate User information and security checks
        if len(email) < 4:
            flash("E-mail must be larger than 3 characters.", category="error")
        elif len(username) < 2:
            flash("Username must be longer than 3 characters.", category="error")
        elif pass1 != pass2:
            flash("Passwords do not match.", category="error")
        elif email_exists(email):
            flash("E-mail already in use", category="error")
        elif username_exists(username):
            flash("Username already in use", category="error")
        else:
            # Encrypt passwd and store
            encpass = bcrypt.hashpw(pass1.encode("utf-8"), bcrypt.gensalt())
            insert_new_user(username, encpass, email) 
            
            # Render login page after successful sign up
            return redirect(url_for("auth.login"))
    
    return render_template("sign_up.html", user=current_user)