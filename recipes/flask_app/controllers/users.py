from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/login', methods = ['POST'])
def user_login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid Email', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Password', 'login')
        return redirect('/')
    session ['id']= user.id
    return redirect('/recipes')


@app.route('/register', methods = ['POST'])
def register_user():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['id'] = id
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')