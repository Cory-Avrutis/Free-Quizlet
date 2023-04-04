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
        numcards = int(request.form.get('num_cards')) 
        card_set = {}
        title = request.form.get(f'title').strip()

        # Ensure user does not have a set with this name already
        if set_exists(current_user.get_id(), title):
            flash('You already have a set with this title.', category='error')
        # Ensure Title not blank
        elif title == '':
            flash('Title for set is blank', category='error')
        else:
            b = 0
            for i in range(1,numcards+1):
                term = request.form.get(f'term_{i}').strip()
                defn = request.form.get(f'definition_{i}').strip()
                
                # Ensure term/defn not blank
                if term == '':
                    flash(f'Term {i} is blank', category='error'); b = 1; break 
                elif defn == '':
                    flash(f'Term {i} is blank', category='error'); b = 1; break

                card_set[term] = defn
            
            # if bad bit not set, push to DB
            if not b:
                insert_new_card_set(card_set, title, current_user.get_id())
    
    return render_template("create_set.html", user=current_user)

# called when clicks on 'View a Set' on home.html
@views.route("/view_sets", methods =['POST', 'GET'])
@login_required
def view_sets():
    # POST  - triggered when user selects a set
    if request.method == 'POST':
        title,set_owner = request.form['info'].split(',')
        cards = get_set_by_user_title(set_owner, title)['Cards']
        return render_template("show_set.html", user=current_user, cards=cards, title=title)

    # GET - by default, displays all sets for viewing
    userSets = get_sets_by_privs('admin') 
    return render_template("view_sets.html", user=current_user, userSets = userSets)

# called when clicks on 'Edit a Set' on home.html 
@views.route("/edit_set", methods = ['POST', 'GET'])
@login_required
def select_set_2_edit():
    # admins can edit any set in existence(NEXXTTTT)
    userSets = get_sets_by_user(current_user.get_id())
    return render_template("view_sets_2_edit.html", user=current_user, userSets = userSets)

# called when user selects set to Edit on view_sets_2_edit.html
@views.route("modify_set", methods = ['POST'])
@login_required
def edit():
    title = request.form['title']
    cards = card_sets.find_one({"User": current_user.get_id(), "Title": title})['Cards']
    return render_template("edit_set.html", user=current_user, cards=cards, title=title)

# called when user clicks title to edit on edit_set.html
@views.route("/edit_title", methods = ['POST'])
@login_required
def edit_title():
    old_title = request.form['old_title']
    new_title = request.form['new_title'].strip()
    f_title = old_title
 
    if new_title == '': 
        flash('Title for set is blank', category='error')
    elif set_exists(current_user.get_id(), new_title):
        flash('You already have a set with this title.', category='error')
    else:
        update_title(current_user.get_id(), old_title, new_title)
    #card_sets.update_one( 
    #    {"User": current_user.get_id(), "Title": old_title}, #query to extract which title
    #    {"$set": {"Title": new_title}}                       #query to update the title
    #    ) 

    
    #cardSet = card_sets.find_one( {"User": current_user.get_id(), "Title": new_title} ) #reset new parameters (cards) for edit_set to render
    cards = get_set_by_user_title(current_user.get_id(), f_title)['Cards']
    #cards = cardSet['Cards']

    return render_template("edit_set.html", user=current_user, cards=cards, title=new_title)
