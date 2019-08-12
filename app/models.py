from app import app, db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.String(500))

class Cart(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.String(500))
