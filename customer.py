from models import customer

def get_user(user):

def get_projects(user):

def getCompleted(user):

def get_activeProjects(user):

def get_last_active(user):


    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    honour_points = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    street_address = db.Column(db.String(100), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    state = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    country = db.Column(db.String(500), nullable=False)
    projects = db.relationship("Projects", backref="customers")
    last_active = db.relationship(db.String(15), nullable=False)