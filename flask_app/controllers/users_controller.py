from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():

    if not User.validate_new_user(request.form):
        return redirect('/')

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }

    user = User.create_user(data)
    
    session['user_id'] = user
    session['first_name'] = request.form['first_name']

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():

    user =  User.get_user_by_email(request.form)

    if not user:
        flash("Email is not registered.")
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password.")
        return redirect('/')

    session['user_id'] = user.id
    session['first_name'] = user.first_name

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    
    session.clear()
    
    return redirect('/')
