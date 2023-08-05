import bcrypt
from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint
from dbmodels import Users, db

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        form_username = request.form["username"].lower()
        form_password = request.form["password"]
        check_username_db = db.session.query(Users).filter(Users.username == form_username).first()
        if not check_username_db or not bcrypt.checkpw(form_password.encode('utf-8'), check_username_db.password.encode('utf-8')):
            flash("Incorrect login or password!", category="error")
        elif check_username_db:
            session["userId"] = check_username_db.id
            session["userDname"] = check_username_db.displayname
            session["userLogged"] = check_username_db.username
            session["userEmail"] = check_username_db.email
            return redirect(url_for("index"))
    return render_template("auth/login.html", title="Login")

@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        form_username = request.form["username"].lower()
        form_displayname = request.form["displayname"]
        form_email = request.form["email"].lower()
        form_password = request.form["password"]
        form_rep_password = request.form["repeat_password"]
        check_username_db = db.session.query(Users).filter(Users.username == form_username).first()
        check_email_db = db.session.query(Users).filter(Users.email == form_email).first()

        if check_username_db:
            flash("This user is already registered!", category="error")
        elif not check_username_db:
            if check_email_db:
                flash("This email is alredy registred!", category="error")
            elif not check_email_db:
                if form_password != form_rep_password:
                    flash("Password mismatch", category="error")
                elif form_password == form_rep_password:
                    hashed_password = bcrypt.hashpw(form_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    db.session.add(Users(
                    username = form_username,
                    displayname = form_displayname,
                    email = form_email,
                    password = hashed_password
                    ))
                    db.session.commit()
                    return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title="Registration")