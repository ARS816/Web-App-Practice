from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.trip import Trip


@app.route('/dashboard')
def trips():
    data = {'id': session['id']}
    return render_template('dashboard.html', user = User.get_one(data), trips = Trip.get_all())

@app.route('/trips/new')
def new_trip():
    data = {'id': session['id']}
    return render_template('new_trip.html', user = User.get_one(data))

@app.route('/trips/new/add', methods=['POST'])
def add_trip():
    if not Trip.validate_trip(request.form):
        return redirect ('/trips/new')
    Trip.save(request.form)
    return redirect('/dashboard')

@app.route('/trips/<int:id>')
def show_trip(id):
    trip = Trip.get_by_id(id) 
    data = {'id': session['id']}
    user = User.get_one(data)
    return render_template('show_trip.html', trip = trip, user = user)

@app.route('/trips/edit/<int:id>')
def edit_trip(id):
    trip = Trip.get_by_id(id)
    data = {'id': session['id']}
    user = User.get_one(data)
    return render_template('edit_trip.html', trip = trip, user = user)

@app.route("/trips/update", methods = ["POST"])
def update():
    if not Trip.validate_trip(request.form):
        return redirect(f"/trips/edit/{request.form['id']}")
    Trip.update(request.form)
    return redirect('/dashboard')

@app.route('/trips/delete/<int:id>')
def delete_post(id):
    Trip.delete(id)
    return redirect('/dashboard')