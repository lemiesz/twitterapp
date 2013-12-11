from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

tweet2user = db.Table('tweet2user',
    db.Column('tweet_id', db.Integer, db.ForeignKey('tweets.uid')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.uid'))
)


class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique = True)
	pwdhash = db.Column(db.String(54))
	tweets = db.relationship('Tweet', secondary=tweet2user,
       		 backref=db.backref('tweets', lazy='dynamic'))

	def __init__(self,firstname,lastname,email,password):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self,password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.pwdhash,password)

class Tweet(db.Model):
	__tablename__ = 'tweets'
	uid = db.Column(db.Integer, primary_key=True)
	tweet = db.Column(db.String(140))
	sentiment = db.Column(db.String(100))
	sentimentValue = db.Column(db.String(20))
	# users = db.relationship('User', secondary=tweet2user,
	# 						backref=db.backref('tweets', lazy='dynamic'))

	def __init__(self,tweet,sentiment,sentimentValue):
		self.tweet = tweet.title()
		self.sentiment = sentiment.title()
		self.sentimentValue = sentimentValue.title()