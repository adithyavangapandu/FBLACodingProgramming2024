from greenpot import db, login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    partners = db.relationship('Partner', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"



class Partner(db.Model):
    __tablename__ = "partner"

    id = db.Column(db.Integer, primary_key=True)
    PartnerName = db.Column(db.String(75), nullable=False)
    Email = db.Column(db.String(120), nullable=True)
    ContactIndividual = db.Column(db.String(100), nullable=True)
    PhoneNumber = db.Column(db.String(20), nullable=True)
    PartType = db.Column(db.String(50), nullable=False)
    Rsc = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Partner('{self.PartnerName}', '{self.Email}', '{self.ContactIndividual}', '{self.PhoneNumber}', '{self.PartType}', '{self.Rsc}')"
    

