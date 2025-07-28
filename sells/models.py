from datetime import datetime
from extentions import db


class Sell(db.Model):
    __tablename__ = 'sells'  # explicit table name
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(100))  

    customer = db.relationship('Customer', backref='sells')
    product = db.relationship('Product', backref='sells')
