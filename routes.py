from idb import app
from flask import render_template, request, flash, session, url_for, redirect
from forms import ContactForm, SignupForm, SigninForm, IncidentsForm
from models import db, User

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
    return redirect(url_for('profile')) 
  
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

@app.route('/profile')
def profile():

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).first()

  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'email' in session:
    return redirect(url_for('profile')) 
      
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
'''
@app.route('/incidents')
def incidents():
	if 'email' not in session:
		return redirect(url_for('signin'))
	user = User.query.filter_by(email = session['email']).first()
	return render_template('incident.html', form = form)
'''
@app.route('/incidents', methods=['GET', 'POST'])
def incidents():
	form = IncidentsForm()
	incidents = []
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('incidents.html', form=form)
		else:
			return 'Form posted.'
	elif request.method == 'GET':
		return render_template('incidents.html', form=form)

