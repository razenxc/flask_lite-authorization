import bcrypt
from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint
from dbmodels import Users, db

bp = Blueprint("accountcp", __name__, url_prefix="/account")

@bp.route("/profile", methods=["POST", "GET"])
def profile():
    if "userLogged" not in session:
        return redirect(url_for("login"))
    
    current_user = db.session.query(Users).filter(Users.username == session["userLogged"]).first()

    # Change account information
    if request.method == "POST":
        try:
            # Change account display name
            if "display_name" in request.form: 
                current_user.displayname = request.form["display_name"]
            # Change account username
            elif "username" in request.form:
                if db.session.query(Users).filter(Users.username == request.form["username"]).first():
                    flash("This username is already occupied")
                else:
                    current_user.username = request.form["username"]
            # Change account email
            elif "email" in request.form:
                if db.session.query(Users).filter(Users.email == request.form["email"]).first():
                     flash("This email is already used")
                else:
                    current_user.email = request.form["email"]
        except Exception as error:
            flash(f"An error occurred while writing to the database: {error}")
        else:
            db.session.commit()
            # If the change in the database was successful, then use the new values in the session
            if "display_name" in request.form:
                session["userDname"] = current_user.displayname
            elif "username" in request.form:
                session["userLogged"] = current_user.username
            elif "email" in request.form:
                session["userEmail"] = current_user.email
    return render_template("profile/profile.html", title=f"{session['userLogged']} profile")

@bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("userId"); session.pop("userDname"); session.pop("userLogged"); session.pop("userEmail")
    return redirect(url_for('index'))