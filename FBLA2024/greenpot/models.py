from greenpot import db, login_manager
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
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
    money = db.Column(db.Float, nullable=True)
    time = db.Column(db.Integer, nullable=True)
    timeframe = db.Column(db.String(20), nullable=True)
    Responsibilities = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    notifications = db.relationship('Notification', backref='notification_partner', lazy=True) 


    def __repr__(self):
        return f"Partner('{self.PartnerName}', '{self.Email}', '{self.ContactIndividual}', '{self.PhoneNumber}', '{self.PartType}', '{self.Rsc}')"
    

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'), nullable=False)
    reminder_type = db.Column(db.String(50), nullable=False)  # Consider using an Enum for predefined types
    message = db.Column(db.String(250), nullable=True)  
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    is_read = db.Column(db.Boolean, nullable=False, default=False)  # Boolean column for read status
    partner = db.relationship('Partner', backref='partner_notifications', lazy=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='user_notifications', lazy=True)

    def __repr__(self):
        return f"Notification('{self.reminder_type}', '{self.message}')"
