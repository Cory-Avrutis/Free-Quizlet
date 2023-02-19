from flask import flash, Blueprint, render_template, request

# Define the "auth" blueprint to handle authorization and security
auth = Blueprint("auth", __name__)

'''
Redirect to the login page
    support GET and POST reguests
'''
@auth.route("/login", methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

'''
Redirect to the logout page
'''
@auth.route("/logout")
def logout():
	return "<p>Logout</p>"

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
        print(email,username,pass1,pass2)    
    
        # Validate User information and security checks
        if len(email) < 4:
            flash("E-mail must be larger than 3 characters.", category="error")
        elif len(username) < 2:
            flash("Username must be longer than 3 characters.", category="error")
        elif pass1 != pass2:
            flash("Passwords do not match.", category="error")
        else:
            # Ensure E-Mail is unique
            # Ensure Username is unique
            # Encrypt passwd and store
            pass
        # return render_template("login.html")
        # Render login page after signing up ?
    return render_template("sign_up.html")

