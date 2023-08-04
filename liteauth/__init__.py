import bcrypt
import os
from flask import Flask, render_template, session, redirect, url_for, request, flash
from dotenv import load_dotenv; load_dotenv()

def app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.getenv("FLASK_SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite"
    )

    # DATABASE
    from flask_sqlalchemy import SQLAlchemy

    db = SQLAlchemy(app)

    class Users(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String, unique=True, nullable=False)
        displayname = db.Column(db.String, nullable=False)
        email = db.Column(db.String, nullable=False)
        password = db.Column(db.String, nullable=False)

    with app.app_context():
        db.create_all()
    # END DATABASE

    # ERRORS HANDLERS
    error_codes = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
        502: "Bad Gateway error",
        503: "Service Unavailable",
        504: "Gateway Timeout error"
    }

    def create_error_handler(code, title):
        @app.errorhandler(code)
        def handle_error(error):
            return render_template("error.html", title=title, error_code=code)
        return handle_error

    for code, title in error_codes.items():
        create_error_handler(code, title)
    # END ERRORS HANDLERS

    @app.route("/")
    def index():
        return render_template("index.html", title="Welcome")

    # Authorization
    @app.route("/login", methods=["POST", "GET"])
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
                return redirect(url_for('index'))
        return render_template("auth/login.html", title="Login")

    @app.route("/register", methods=["POST", "GET"])
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
                        return redirect(url_for("login"))
        return render_template("auth/register.html", title="Registration")
    
    # Profile
    @app.route("/profile")
    def profile():
        if "userLogged" not in session:
            return redirect(url_for("login"))
        return render_template("profile/profile.html", title=f"{session['userLogged']} profile")
    
    @app.route("/change_display_name", methods=["POST"])
    def change_display_name():
        if request.method == "POST":
            flash("Error (/change_display_name)", category="error")
        return redirect(url_for('profile'))

    @app.route("/change_username", methods=["POST"])
    def change_username():
        if request.method == "POST":
            flash("Error (/change_username)", category="error")
        return redirect(url_for('profile'))
    
    @app.route("/change_email", methods=["POST"])
    def change_email():
        if request.method == "POST":
            flash("Error (/change_email)", category="error")
        return redirect(url_for('profile'))

    @app.route("/logout", methods=["POST", "GET"])
    def logout():
        session.pop("userId"); session.pop("userDname"); session.pop("userLogged"); session.pop("userEmail")
        return redirect(url_for('index'))

    return app