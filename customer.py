from models import customer
from flask import Flask, render_template, redirect, request, flash, abort, session, jsonify

def get_user(user):
    user = db.session.query(Customer).filter(Customer.email == email).first()
    pass
def get_projects(user):
    pass
def getCompleted(user):
    pass
def get_activeProjects(user):
    pass
def get_last_active(user):
    pass