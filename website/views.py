from flask import Blueprint, flash, url_for, redirect, render_template, request
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

'''
Redirects to the create a new card set page
Handles the POST when user submits new set to add
'''
@views.route("/create_set", methods =['POST', 'GET'])
@login_required
def create_set():
    if request.method == 'POST':

        user = User(current_user)

        numcards = int(request.form.get('num_cards')) 

        card_set = {}

        title = request.form.get(f'title')
            
        # Ensure Title not blank
        if title == '':
            flash('Title for set is blank', category='error')
        else:
            b = 0        
            for i in range(1,numcards+1):
                term = request.form.get(f'term_{i}')
                defn = request.form.get(f'definition_{i}')
                
                # Ensure term/defn not blank
                if term == '':
                    flash(f'Term {i} is blank', category='error'); b = 1; break 
                elif defn == '':
                    flash(f'Term {i} is blank', category='error'); b = 1; break

                card_set[term] = defn
            
            # if bad bit not set, push to DB
            if not b:
                print(card_set)
                insert_new_card_set(card_set, title, current_user.get_id())
    
    return render_template("create_set.html", user=current_user)

