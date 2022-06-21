from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.login import Login
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def start_page():
    return render_template("index.html")

@app.route("/create", methods = ['POST'])
def create_login():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    login = {
            "first_name" : request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"]
    }
    errors = False
    
    if len(request.form['first_name']) < 2:
        flash('First Name must be at least 2 characters', 'first_name')
        errors = True
    if len(request.form['last_name']) < 2:
        flash('Last Name must be at least 2 characters', 'last_name')
        errors = True
    if not request.form['password'] == request.form['password_confirm']:
        flash("Passwords do NOT match; please try again", 'password_error')
        errors = True
    if not Login.validate_email(login):
        errors = True
    
    if len(request.form['password']) < 6:
        flash('Password must be 6 characters long!', 'password_length')
        errors = True

    if errors:
        return redirect ('/')
    
    login = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        'password' : pw_hash
    }
    Login.create_login(login)
    login = Login.get_one_email(login)
    return redirect(f"/user/page/{login.id}")

@app.route("/login", methods=['POST'])
def login():
    data = {'email' : request.form['email_login']}
    user_in_db = Login.get_one_email(data)

    if not user_in_db:
        flash('Invalid Email/Password', 'login_error')
        return redirect('/')
    elif not bcrypt.check_password_hash(user_in_db.password, request.form['password_login']):
        flash('Invalid Email/Password', 'login_error')
        return redirect('/')
    session['id'] = user_in_db.id

    return redirect(f"/user/page/{user_in_db.id}")

@app.route('/user/page/<int:id>')
def display_user_page(id):
    data = {'id' : id}
    login = Login.get_one_id(data)
    print(login)
    return render_template('display_page.html', login=login)
