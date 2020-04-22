from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ArrowType
from sqlalchemy import create_engine 
import arrow
from flask import Flask, render_template, redirect, request, flash, abort, session, jsonify

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = 'Bbklct321'

class customer(db.Model):
    """List of customers"""
    __tablename__ = "customers"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(500), nullable=False)
    street_address = db.Column(db.String(100), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    state = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    country = db.Column(db.String(500), nullable=False)
    honour_points = db.Column(db.Integer, nullable=True,default=100)
    likes = db.Column(db.Integer,nullable=True,default=0)
    dislikes = db.Column(db.Integer,nullable=True,default=0)
    reviews = db.relationship("Reviews", backref="customers")
    projects = db.relationship("Projects", backref="customers")

    def __repr__(self):

        return "<Customer id={}, first_name={}, last_name={}, email={}>".format(self.user_id,
                                                                                self.first_name,
                                                                                self.last_name,
                                                                                self.email)
class Projects(db.Model):
    """List of projects"""
    __tablename__ = "projects"

    user_id = db.Column(db.Integer, db.ForeignKey("customers.user_id"), nullable=False)
    project_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    project_name = db.Column(db.String(500), nullable = False)
    project_description = db.Column(db.String(10000), nullable = True)
    project_completed = db.Column(db.Integer, nullable = False, default = 0)

class Reviews(db.Model):
    review_id = db.Column(db.Integer, nullable = False, primary_key = True )
    user_id = db.Column(db.Integer, nullable=False)
    maker_id = db.Column(db.Integer, db.ForeignKey("customers.user_id"), nullable=False)
    description = db.Column(db.String(10000), nullable = True)
    recommend = db.Column(db.String(1000), nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)



def connect_to_db(app, database='postgresql://postgres:Bbklct321@localhost:5432/artistic'):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
