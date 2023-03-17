from flask import Blueprint, url_for, redirect, render_template, request
from flask_login import login_required, current_user


# Define a blueprint called "views" for webpage viewing
views = Blueprint("views", __name__)

''' 
Redirects to main page with user if logged in 
'''
@views.route("/", methods =['POST', 'GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/create_set", methods =['POST', 'GET'])
@login_required
def create_set():
    if request.method == 'POST':
        numcards = int(request.form.get('num_cards'))    
        card_set = {}
        for i in range(1,numcards+1):
            term = request.form.get(f'term_{i}')
            defn = request.form.get(f'definition_{i}')
            card_set[term] = defn
        print(card_set)
    return render_template("create_set.html", user=current_user)

