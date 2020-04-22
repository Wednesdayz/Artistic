from flask import Flask, render_template, redirect, request, flash, abort, session, send_from_directory, abort
from flask.json import jsonify
import json
from flask_mail import Mail, Message
import os
from jinja2 import StrictUndefined
from models import *
from passlib.hash import pbkdf2_sha256
import cards

app = Flask(__name__)
app.secret_key = 'Bbklct321'

app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

@app.route('/')
def homepage():
    """Display Homepage"""
    
    return render_template("homepage.html")

@app.route('/login', methods=['POST'])
def process_login():
    """Process login data. Add user_id to session"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(customer).filter(customer.email == email).first()

    if user and pbkdf2_sha256.verify(password, user.password_hash):

        session['email'] = email
        if session.get('email'):
            flash("Login successful!")
            return "Success"    
        else:
            return "CookieFail"

    else:

        return "Fail"

@app.route('/logout')
def process_logout():
    """Log user out, redirect to /products"""

    del session['email']

    flash("You have been logged out.")

    return redirect("/")

@app.route('/register')
def show_register():
    """Show registration form"""

    return render_template("register.html")

@app.route('/register', methods=['POST'])
def process_registration():
    """Process user registration"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    password = pbkdf2_sha256.encrypt(password, rounds=20000, salt_size=16)
    phone = request.form.get("phone")
    street_address = request.form.get("street_address")
    zipcode = request.form.get("zipcode")
    state = request.form.get("state")
    country = request.form.get("country")

    user = customer(first_name=first_name, last_name=last_name, email=email, password_hash=password, phone=phone,street_address=street_address, zipcode=zipcode, state=state, country=country)
    
    db.session.add(user)
    db.session.commit()

    session['email'] = email
    if session.get('email'):
        flash("Registration successful! Welcome to Beyond")
    else:
        flash("Please enable cookies to log in")

    return redirect("/")
@app.route('/projects')
def projects():
    """Display projects page"""
    projects = db.session.query(Projects)
    return render_template("projects.html", projects = projects)

@app.route('/account')
def account():
    """Display Account page"""
    if session.get('email'):
        customers = db.session.query(customer).filter(customer.email == session['email']).one()
        return render_template("account.html", customers = customers)
    else:
        flash('Please login')
        return redirect('/')

@app.route('/create')
def create():
    """create new project"""
    if session.get('email'):
        customers = db.session.query(customer).filter(customer.email == session['email']).one()
        return render_template("create_new.html", customers = customers)
    else:
        flash('Please login')
        return redirect('/')


@app.route('/create_project', methods=['POST'])
def create_project():
    """Process user project creation"""

    user_id = db.session.query(customer).filter(customer.email == session['email']).one()
    project_name = request.form.get("project_name")
    project_description = request.form.get("project_description")
    project_completed = 0
    new_project = Projects(user_id = user_id.user_id, project_name = project_name, project_description = project_description, project_completed = project_completed)
    print("hello")
    db.session.add(new_project)
    db.session.commit()
    flash('Project Created')
    return redirect("/")


@app.route('/KanbanBoard')
def index():
    """Serve the main index page"""
    return send_from_directory('templates', 'kanban.html')

@app.route('/static/<path:path>')
def static_file(path):
    """Serve files from the static directory"""
    return send_from_directory('static', path)

@app.route('/cards')
def get_cards():
    """Get an order list of cards"""
    return json.dumps(cards.all_cards())

@app.route('/columns')
def get_columns():
    """Get all valid columns"""
    return json.dumps(app.config.get('kanban.columns'))

@app.route('/card', methods=['POST'])
def create_card():
    """Create a new card"""

    # TODO: validation
    cards.create_card(
        text=request.form.get('text'),
        column=request.form.get('column', app.config.get('kanban.columns')[0]),
        color=request.form.get('color', None),
    )

    # TODO: handle errors
    return 'Success'

@app.route('/card/reorder', methods=["POST"])
def order_cards():
    """Reorder cards by moving a single card
    The JSON payload should have a 'card' and 'before' attributes where card is
    the card ID to move and before is the card id it should be moved in front
    of. For example:
      {
        "card": 3,
        "before": 5,
      }
    "before" may also be "all" or null to move the card to the beginning or end
    of the list.
    """
    cards.order_cards(request.get_json())
    return 'Success'


@app.route('/card/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    """Update an existing card, the JSON payload may be partial"""

    # TODO: handle errors
    cards.update_card(card_id, request.get_json(), app.config.get('kanban.columns'))

    return 'Success'

@app.route('/card/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    """Delete a card by ID"""

    # TODO: handle errors
    cards.delete_card(card_id)
    return 'Success'




if __name__ == "__main__":
    # Change app.debug to False before launch
    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")