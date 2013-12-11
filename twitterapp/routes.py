from twitterapp import app
from flask import Flask, render_template, request, flash, session, redirect, url_for, Response
from models import db, User, Tweet
from sqlalchemy import func
from forms import SignupForm, SigninForm
from TwitterAPI import TwitterAPI
import json
#app = Flask(__name__)

print 'hello world'
user = ""

@app.route('/')
def index():
	return render_template('layout.html')

@app.route('/testdb')
def testdb():
	if db.session.query("1").from_statement("SELECT 1").all():
		return 'It works.'
	else:
		return 'Something is broken.'
@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/post/tweet',methods=['POST','GET'])
def addTweets():
	data = json.loads(request.data)
	tweets = []
	if 'email' not in session:
		return redirect(url_for('signin'))
	user = User.query.filter_by(email = session['email']).first()

	for item in data:
		tweetText = item['tweet']
		sentiment = item['data']['type']
		sentimentValue = item['data']['score']
		tweet = Tweet(tweetText.encode('ascii','ignore'),sentiment,str(sentimentValue).encode('ascii','ignore'))
		tweets.append(tweet)
		user.tweets.append(tweet)
	
	db.session.commit()

	return redirect(url_for('profile'))

@app.route('/get/userTweets')
def getUserTweets():
	if 'email' not in session:
		return redirect(url_for('signin'))
	user = User.query.filter_by(email = session['email']).first()
	returnVal = []
	for tweet in user.tweets:
		returnVal.append(to_json(tweet))
	return Response(json.dumps(returnVal),mimetype='application/xml')
	
@app.route('/get/avgSen')
def getAverageSentiment():
	cur = db.session.query(func.avg(Tweet.sentimentValue).label('senVale'))
	for item in cur.all():
		return json.dumps(item)

@app.route('/twitter')
def twit():
	return render_template('twit.html')

@app.route('/post/mzb', methods=['POST','GET'])
def mzbpost():
	values = json.loads(request.data)
	user = values['user']
	return _getTweets(user)


@app.route('/delete',methods=['GET'])
def deleteUser():
	userEmail = session['email']
	user = User.query.filter_by(email = userEmail.lower()).first()
	db.session.delete(user)
	db.session.commit()
	return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:   
			newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
     		db.session.add(newuser)
     		db.session.commit()
       		session['email'] = newuser.email
       	     	return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/signin',methods=['GET','POST'])
def signin():
	form = SigninForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	return redirect(url_for('home'))

@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))
	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')


@app.route('/login/checkLogin')
def checkLogin():
	data = {'isLogin': False, 'uid': 0}
	data['isLogin'] = False;
	if 'email' not in session:
		return Response(json.dumps(data), mimetype='application/json')
	user = User.query.filter_by(email = session['email']).first()
	if user is None:
		return Response(json.dumps(data), mimetype='application/json')
	else:
		data['isLogin'] = True
		data['uid'] = user.uid
		return Response(json.dumps(data), mimetype='application/json')

@app.route('/getTweets')
def getTweets():
	return _getTweets(user)


def _getTweets(user):
	api = TwitterAPI("aiC1HsGnI81CrWQ78ejw","244t73B6eDybGbxPrqcxfXMjdfy3OBeqKndcnBakE5M","237561704-JIg6SthgLfZge8naa7Pun3ANpSo3r0BprtlrLFto","7FGLhL5UFW0F1RWRraF3HqPvY5cvhmOXMQt2FKjxC0")
	r = api.request('statuses/user_timeline', {'screen_name':user})
	tempList = []
	for item in r:
		tempObj = item['text']
		tempList.append(tempObj)
	return Response(json.dumps(tempList),  mimetype='application/json')


def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object.
    """
    json1 = {}
    json1['pk'] = getattr(model, 'uid')
 
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        json1[col.name] = getattr(model, col.name)
 
    return json.dumps(json1)

# @app.route('/post/user',methods=['POST','GET'])
# def saveuser():
# 	data = json.loads(request.data)
# 	firstname = data['firstname']
# 	lastname = data['lastname']
# 	email = data['email']
# 	password = data['password']
# 	newuser = User(firstname,lastname,email,password)

# 	db.session.add(newuser)
# 	db.session.commit()
# 	return home()
