from db import db

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), nullable = False)
    mobile = db.Column(db.String(80), nullable = False)
    message = db.Column(db.String(120), nullable = False)