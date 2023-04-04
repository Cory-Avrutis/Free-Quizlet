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

@views.route("/view_sets", methods =['POST', 'GET'])
@login_required
def view_sets():
    userSets = []

    print("user id is ", current_user.get_id())
    for setCurr in card_sets.find({"User": current_user.get_id()}):
        userSets.append(setCurr)
        print(setCurr)
            
    return render_template("view_sets.html", user=current_user, userSets = userSets)


@views.route("/show_set", methods =['POST', 'GET'])
@login_required
def select_set():
    title = ""
    if request.method == 'POST':
        title = request.form['title']

    cardSet = card_sets.find_one( {"User": current_user.get_id(), "Title": title} )
    cards = cardSet['Cards']
    return render_template("show_set.html", user=current_user, cards=cards, title=title)


@views.route("/edit_set", methods = ['POST', 'GET'])
@login_required
def select_set_2_edit():
    userSets = []

    for setCurr in card_sets.find({"User": current_user.get_id()}): #
        userSets.append(setCurr)
        print(setCurr)
            
    return render_template("view_sets_2_edit.html", user=current_user, userSets = userSets)


@views.route("modify_set", methods = ['POST', 'GET'])
@login_required
def edit():
    title = ""
    if request.method == 'POST':
        title = request.form['title']

    cardSet = card_sets.find_one( {"User": current_user.get_id(), "Title": title} )
    cards = cardSet['Cards']

    return render_template("edit_set.html", user=current_user, cards=cards, title=title)

@views.route("/edit_title", methods = ['POST', 'GET'])
@login_required
def edit_title():
    old_title = ""
    new_title = ""

    if request.method == 'POST':
        old_title = request.form['old_title']
        new_title = request.form['new_title']


    card_sets.update_one( 
        {"User": current_user.get_id(), "Title": old_title}, #query to extract which title
        {"$set": {"Title": new_title}}                       #query to update the title
        ) 

    
    cardSet = card_sets.find_one( {"User": current_user.get_id(), "Title": new_title} ) #reset new parameters (cards) for edit_set to render
    cards = cardSet['Cards']

    return render_template("edit_set.html", user=current_user, cards=cards, title=new_title)

@views.route("/edit_term", methods = ['POST', 'GET'])
@login_required
def edit_term():

    title = ""
    old_term = ""
    new_term = ""
    
    if request.method == 'POST':
        title = request.form['title']
        old_term = request.form['old_term']
        new_term = request.form['new_term']

    print("My test\nThe old title retrieved is ", old_term)
    print("The new title retrieved is ", new_term)

    cardSet = card_sets.find_one( {"User": current_user.get_id(), "Title": title} ) # find set that needs editing
    cards = cardSet['Cards']
    

   
    #To Mariela, 
    #what happens in if the new term is a term that already exists? 
    #do we need to add error handling, is it an automatic reject by Mongo, or does it not even matter? 
    # - Steven

    """
    some discoveries on above
    1) updated term being the same as its old term leads to the card being deleted (handled with if old_term != new_term)

    2) updated term being the same as another term already in the set leads to undefined behavior. 
     usually deletes both old and other shared card with same term, sometimes does nothing, and rarely will fatally crash website
       (for Mariela to do. i assume something like if new term is not in cards_terms. put it with the if condition below)



    3) not a dangeorus bug. when a card is updated, it is appended at the end of the data structure. this reorders it differently when edit_set renders
        could be fixed. could also be left as is

        - Steven
    """

    if old_term != new_term:

        # add new card with new ter, use existing definiton
        card_sets.update_one({"User": current_user.get_id(), "Title": title}, {"$set": {'Cards.' + new_term: cards[old_term]}})     #adds new term, matches it with old definition
        card_sets.update_one({"User": current_user.get_id(), "Title": title}, {"$unset": {'Cards.' + old_term: cards[old_term]}})   #gets rid of the previous term and its definition
    
    cardSet = card_sets.find_one( {"User": current_user.get_id(), "Title": title} ) # finds the updated cards to be sent to edit_set.html 
    cards = cardSet['Cards']
    
    return render_template("edit_set.html", user=current_user, cards=cards, title=title)


@views.route("/edit_definition", methods = ['POST', 'GET'])
@login_required
def edit_definition():

    title = ""
    term = ""
    old_def = ""
    new_def =""
    
    if request.method == 'POST':
        title = request.form['title']
        term = request.form['term']
        old_def = request.form['old_def']
        new_def = request.form['new_def']

    """
    To Mariela,

    please also handle error checking to make sure new definition is not already a definition in the set

     thank you! - Steven
    """
    
    if old_def != new_def:
        card_sets.update_one({"User": current_user.get_id(), "Title": title}, {"$unset": {'Cards.' + term: old_def}})     #gets rid of the previous term and its definition
        card_sets.update_one({"User": current_user.get_id(), "Title": title}, {"$set": {'Cards.' + term: new_def}})       #adds new term, matches it with old definition     

    cardSet = card_sets.find_one( {"User": current_user.get_id(), "Title": title} ) # resets the updates cards to be sent to edit_set.html 
    cards = cardSet['Cards']
    
    return render_template("edit_set.html", user=current_user, cards=cards, title=title)