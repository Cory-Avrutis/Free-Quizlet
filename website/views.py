from flask import Blueprint, url_for, redirect, render_template, request
from flask_login import login_required, current_user

from .models import User
from .database import *

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

        user = User(current_user)

        numcards = int(request.form.get('num_cards')) 

        card_set = {}

        title = request.form.get(f'title')
        for i in range(1,numcards+1):
            term = request.form.get(f'term_{i}')
            defn = request.form.get(f'definition_{i}')

            if term != "" and defn != "" and title != "":
                card_set[term] = defn

            if i == numcards: #last iteration
                print("Numcards is ", numcards)
                print("i is ", i)
                print(card_set)
                insert_new_cards(card_set, title, current_user.get_id())
        
    return render_template("create_set.html", user=current_user)

