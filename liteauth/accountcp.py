import bcrypt
from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint
from dbmodels import Users, db

bp = Blueprint("accountcp", __name__, url_prefix="/account")

@bp.route("/profile")
def profile():
    if "userLogged" not in session:
        return redirect(url_for("login"))
    return render_template("profile/profile.html", title=f"{session['userLogged']} profile")

@bp.route("/change_display_name", methods=["POST"])
def change_display_name():
    if request.method == "POST":
        flash("Error (/change_display_name)", category="error")
    return redirect(url_for('profile'))

@bp.route("/change_username", methods=["POST"])
def change_username():
    if request.method == "POST":
        flash("Error (/change_username)", category="error")
    return redirect(url_for('profile'))

@bp.route("/change_email", methods=["POST"])
def change_email():
    if request.method == "POST":
        flash("Error (/change_email)", category="error")
    return redirect(url_for('profile'))

@bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("userId"); session.pop("userDname"); session.pop("userLogged"); session.pop("userEmail")
    return redirect(url_for('index'))