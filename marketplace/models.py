from . import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Blueprint, render_template, url_for, flash, redirect, Flask
from flask_login import UserMixin

class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), unique = True, nullable = False)
        email = db.Column(db.String(120), unique = True, nullable = False)
        password = db.Column(db.String(60), nullable = False)
        shoes = db.relationship('Shoe', backref = 'seller', lazy=True)
        bids = db.relationship('Bid', backref = 'bidder', lazy=True)
        def __repr__(self):
                return f"User('{self.username}', '{self.email}'')"


class Shoe(db.Model):
        __searchable__ = ['name', 'description']
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), nullable = False)
        brand = db.Column(db.String(120), nullable = False)
        size = db.Column(db.String(120), nullable = False)
        condition = db.Column(db.String(20), nullable = False)
        colour_way = db.Column(db.String(120), nullable = False)
        description = db.Column(db.Text, nullable = False)
        price = db.Column(db.Integer, nullable = False)
        style = db.Column(db.String(120), nullable = False)
        image_file = db.Column(db.String(20), nullable = False)
        date_posted = db.Column(db.DateTime, nullable = False, default = datetime.now())
        sold_status = db.Column(db.Boolean, nullable = False, default = False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
        bids = db.relationship('Bid', backref = 'bids', lazy = True)
        def __repr__(self):
                return f"User('{self.name}', '{self.price}', '{self.date_posted}'')"

class Bid(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        amount = db.Column(db.Integer, nullable = False)
        status = db.Column(db.String(20), nullable = False, default = "New")
        phone_number = db.Column(db.String(20), nullable = False)
        date_posted = db.Column(db.DateTime, nullable = False, default = datetime.now())
        sold_date = db.Column(db.DateTime)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
        shoe_id = db.Column(db.Integer, db.ForeignKey('shoe.id'), nullable = False)
