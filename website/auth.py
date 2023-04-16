from flask import url_for, flash, Blueprint, render_template, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from .database import *
from .models import User
import bcrypt

# Define the "auth" blueprint to handle authorization and security
auth = Blueprint("auth", __name__)


# route to account management (admin only)
@auth.route('/accounts', methods=['GET','POST'])
@login_required
def manage_accounts():
    ausers = get_users('admin')
    musers = get_users('mod')
    users = get_users('user')
    return render_template('accounts.html',user=current_user, ausers=ausers,musers=musers,users=users)    

# delete an account
@auth.route("/delete_acc", methods = ['POST'])
@login_required
def delete_account():
    d_user = request.form.get('user')
    ausers = get_users('admin')
    musers = get_users('mod')
    users = get_users('user')
    delete_user(d_user)
    if d_user == current_user.username:
        flash("Account deleted. You have been logged out.", category="success")
        logout_user()
        return redirect(url_for("auth.login"))
    else:
        s = f'Account \'' + d_user + '\' deleted.'
        flash(s,  category="success")
    return render_template('accounts.html',user=current_user, ausers=ausers,musers=musers,users=users)    

# change privileges for an account
@auth.route("/change_priv", methods = ['POST'])
@login_required
def change_privs():
    p_user = request.form.get('user')
    new_priv = request.form.get('privilege')
    ausers = get_users('admin')
    musers = get_users('mod')
    users = get_users('user')
    change_user_privs(p_user, new_priv)
    s = 'Account \'' + p_user + '\' now has privilege level : \'' + new_priv + '\'.'
    flash(s, category="success")
    return render_template('accounts.html',user=current_user, ausers=ausers,musers=musers,users=users)    



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
