from flask import Blueprint, flash, url_for, redirect, render_template, request
from flask_login import login_required, current_user

from .models import User
from .database import *
from quizFunc import *

import copy     #to make a copy of the dictionary for write
from collections import OrderedDict #to make that copied dictionary in order
import html   #part of the JavaScript fix for recognizing special characters being sent back to backend

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
    # POST  - triggered when user selects a set to view
    if request.method == 'POST':
        mode = request.args.get("id")

        title,set_owner = request.form['info'].split(',')

        print("The title from view_sets ", title)

        cards = get_set_by_user_title(set_owner, title)['Cards']
        if mode == "flashcard":
            return render_template("show_set.html", user=current_user, cards=cards, title=title)
        elif mode == "quiz":
            questions = []
            if (validQuiz(cards) == True):
                questions = createQuiz(cards)
            else:
                flash('Unable to create quiz for set. Please make sure there are at least two cards with unique definitions.', category='error')
            print("questions is: ", questions)
            return render_template("quiz_set.html", user=current_user, questions=questions, title=title, total=len(questions))
        elif mode == "write":
            if len(cards) < 1 :
                flash('Unable to create write mode for set. Please make sure there is at least one card in the set.', category='error')
            else:

                #bit different for write mode. instead of sending all the cards at once, i just want the first one
                #then when user is done with first, i'll reload render_template with the second one. similiar logic for when they finish the second
                #repeat this logic until i iterate through all the cards

                copy_and_ordered = copy.deepcopy(cards)
                copy_and_ordered = OrderedDict(sorted(copy_and_ordered.items())) 

                first_card_term = list(copy_and_ordered.keys())[0]            
                return render_template("write_set.html", set_owner=set_owner, user=current_user, title=title, card_term = first_card_term, currentIndex = 0, cards = copy_and_ordered)
            #start coding here 
            # return render_template("write.html", user=current_user, cards=cards, title=title)

    # GET - by default, displays all sets for viewing
    userSets = get_sets_by_privs('admin') 
    return render_template("view_sets.html", user=current_user, userSets = userSets)

@views.route("/next-card", methods = ['POST', 'GET'])   
@login_required
def next_card():
    #to be used after write_set.html firsts get called from views.set

    
    set_owner = request.form['set_owner']
    title = request.form['title']
    title = html.unescape(title)

    current_index = int(request.form['current_index'])

    print("The current index is ", current_index)
    

    print("The set owner is ", set_owner)
    print("The title is ", title)
    
    cards = get_set_by_user_title(set_owner, title)['Cards'] 

    print("The cards are ", cards)           
    copy_and_ordered = copy.deepcopy(cards)
    copy_and_ordered = OrderedDict(sorted(copy_and_ordered.items()))


    print("The length of the dictionary is ", len(copy_and_ordered))

    if current_index < len(copy_and_ordered) - 1:
        current_index = current_index + 1
        next_card = list(copy_and_ordered.keys())[current_index]            
    
        #render the next card's definition for the user to type
        #need to talk to Cory about the user = current_user
        #do i need to like pass the user as a form request ? or can i just do what i did below because of the @login required thing

        #i should do a pull (push ?) request to clear up a lot of these "should i" regarding set_owner and current_usr. it looks like
        # it's part of cory's code domain, which i am not entirely sure the ins and outs of

        print("It got up to here")

        return render_template("write_set.html", set_owner=set_owner, user=current_user, title = title, card_term = next_card, currentIndex = current_index, cards = copy_and_ordered)
    else:
        #if there are no more cards, redirect the user to the home page 
        return render_template("home.html", user=current_user)



# called when clicks on 'Edit a Set' on home.html 
@views.route("/edit_set", methods = ['POST', 'GET'])
@login_required
def edit_sets():
    # if POST --> user selected a set to EDIT
    if request.method == 'POST':
        title,set_owner = request.form['info'].split(',')
        cards = get_set_by_user_title(set_owner,title)['Cards']
        return render_template("edit_set.html", user=current_user, set_owner=set_owner, cards=cards, title=title)
    # When editing sets:
    #   admin = edit all sets (All Users, All Admin, All Mod , Own Sets)  
    #   mod = edit Own and all User sets (All Users, Own Sets)
    #   user = edit Own sets (Own)
    if get_user_privs(current_user.get_id()) == 'admin':
        userSets = get_sets_by_privs('admin')
    elif get_user_privs(current_user.get_id()) == 'mod':
        userSets = get_sets_by_privs('mod', current_user.get_id())
    elif get_user_privs(current_user.get_id()) == 'user':
        userSets = get_sets_by_privs('user', current_user.get_id())
    return render_template("view_sets_2_edit.html", user=current_user, userSets = userSets)

# called when user changes title for a set
@views.route("/edit_title", methods = ['POST'])
@login_required
def edit_title():
    old_title = request.form['old_title']
    new_title = request.form['new_title'].strip()
    set_owner = request.form['set_owner'].strip()
    f_title = old_title     # final title (for page re-rendering)
 
    if new_title == '': 
        flash('Title for set is blank', category='error')
    elif set_exists(current_user.get_id(), new_title):
        flash('You already have a set with this title.', category='error')
    else:
        f_title = new_title
        update_title(set_owner, old_title, new_title)
    cards = get_set_by_user_title(set_owner, f_title)['Cards'];print(set_owner,f_title)
    return render_template("edit_set.html", set_owner=set_owner, user=current_user, cards=cards, title=f_title)

@views.route("/edit_term", methods = ['POST'])
@login_required
def edit_term():
    title = request.form['title']
    old_term = request.form['old_term']
    new_term = request.form['new_term']
    set_owner = request.form['set_owner'].strip()
    cards = get_set_by_user_title(set_owner, title)['Cards']

    #To Mariela, 
    #what happens in if the new term is a term that already exists? 
    #do we need to add error handling, is it an automatic reject by Mongo, or does it not even matter? 
    # - Steven

    """
    some discoveries on above
    1) updated term being the same as its old term leads to the card being deleted 
        (handled with if old_term != new_term)

    2) updated term being the same as another term already in the set leads to undefined behavior. 
     usually deletes both old and other shared card with same term, sometimes does nothing, and rarely will fatally crash website
       (for Mariela to do. i assume something like if new term is not in cards_terms. put it with the if condition below)

    3) not a dangeorus bug. when a card is updated, it is appended at the end of the data structure. this reorders it differently when edit_set renders
        (could be fixed. could also be left as is)
        - Steven
    """

    if old_term == new_term:
        flash('Unable to edit term. No change detected.', category='error')
    elif new_term in cards:
        flash('Term already exists in the set.', category='error')
    else:
        replace_term(set_owner,title,new_term,old_term)
    
    # updated cardset to show when screen reloads
    cards = get_set_by_user_title(set_owner,title)['Cards'] 
    return render_template("edit_set.html", set_owner=set_owner,user=current_user, cards=cards, title=title)


@views.route("/edit_definition", methods = ['POST'])
@login_required
def edit_definition():
    title = request.form['title']
    term = request.form['term']
    old_def = request.form['old_def']
    new_def = request.form['new_def']
    set_owner = request.form['set_owner'].strip()


    # updated cardset to show when screen reloads
    cards = get_set_by_user_title(set_owner, title)['Cards']
    #cardSet = card_sets.find_one( {"User": current_user.get_id(), "Title": title} ) # finds the updated cards to be sent to edit_set.html 
    #cards = cardSet['Cards']

    if old_def != new_def and new_def in cards.values():
        flash('Warning: Existing term has same definition', category='warning')
    if old_def == new_def:
        flash('Unable to edit definition. No change detected.', category='error')
    else:
        replace_definition(set_owner,title,term,new_def,old_def)

    cards = get_set_by_user_title(set_owner, title)['Cards']
    
    return render_template("edit_set.html", set_owner=set_owner, user=current_user, cards=cards, title=title)

@views.route("/new_card", methods = ['POST'])
@login_required
def new_card():
    title = request.form['title']
    new_term = request.form['new_term']
    new_def = request.form['new_def']
    set_owner = request.form['set_owner']

    """
    To Mariela,
        Please handle error checking again to make sure new term (updated term) is not already in the set.

    Thank you! - Steven
    """
    cards = get_set_by_user_title(set_owner, title)['Cards']
    
    if new_def in cards.values():
        flash('Warning: Existing term has same definition', category='warning')
    if new_term in cards:
        flash('Unable to add. Term already exists in the set.', category='error')
    elif new_term == "" or new_def == "":
        flash('Unable to add. Term or definition was left empty.', category='error')
    #only neccessary for add a card because i wrapped the form around both inputs. if they click out, flow goes here so must error check
    else:
        insert_card(set_owner,title,new_term,new_def)
        #card_sets.update_one(
        #    {"User": current_user.get_id(), "Title": title}, 
        #    {"$set": {'Cards.' + new_term: new_def}})       #adds new term with its new definition    

    cards = get_set_by_user_title(set_owner, title)['Cards']
    return render_template("edit_set.html", set_owner=set_owner,user=current_user, cards=cards, title=title)

@views.route("/delete_card", methods = ['POST'])
@login_required
def delete_card():
    title = request.form['title']
    _term = request.form['old_term']
    _def = request.form['old_def']
    set_owner = request.form['set_owner']
    
    """
    To Mariela,
        No error handling requried here :-)
    - Steven
    """
    
    delete_card_from_set(set_owner, title, _term, _def)
    cards = get_set_by_user_title(set_owner, title)['Cards']
    return render_template("edit_set.html", set_owner=set_owner, user=current_user, cards=cards, title=title)

@views.route("/delete_set", methods = ['POST'])
@login_required
def delete_set():
    title = request.form['title']
    set_owner = request.form['set_owner']
    print("deleting ", title, "created by ", set_owner) 
    delete_card_set(set_owner, title) 
    if get_user_privs(current_user.get_id()) == 'admin':
        userSets = get_sets_by_privs('admin')
    elif get_user_privs(current_user.get_id()) == 'mod':
        userSets = get_sets_by_privs('mod', current_user.get_id())
    elif get_user_privs(current_user.get_id()) == 'user':
        userSets = get_sets_by_privs('user', current_user.get_id())
    return render_template("view_sets_2_edit.html", user=current_user, userSets = userSets)

