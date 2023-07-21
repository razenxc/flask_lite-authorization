from flask import Flask, render_template, session, redirect, url_for, request, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "q$1w2e$3r4t_5y6=^u7i8&o9p"

# DATABASE
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()
# END DATABASE

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", title="Error 404", error_code=404)

@app.route("/")
def index():
    return render_template("index.html", title="Welcome")

@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        form_username = request.form["username"]
        form_password = request.form["password"]
        check_auth_data_db = Users.query.filter_by(username=form_username, password=form_password).first()

        if not check_auth_data_db:
            flash("Incorrect login or password!", category="error")
        elif check_auth_data_db:
            session["userLogged"] = request.form["username"]
            return redirect(url_for('index'))
    return render_template("auth/login.html", title="Login")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        form_username = request.form["username"]
        form_email = request.form["email"]
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
                    db.session.add(Users(
                    username = form_username,
                    email = form_email,
                    password = form_password
                    ))
                    db.session.commit()
                    return redirect(url_for("login"))
    return render_template("auth/register.html", title="Registration")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop('userLogged')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)