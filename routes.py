from flask import Flask, render_template, redirect, request, flash, abort, session, jsonify
from flask_mail import Mail, Message
import os
from jinja2 import StrictUndefined
from models import *
from passlib.hash import pbkdf2_sha256

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
    return render_template("projects.html")

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




if __name__ == "__main__":
    # Change app.debug to False before launch
    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")