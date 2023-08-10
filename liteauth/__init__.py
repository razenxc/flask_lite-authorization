import os
from flask import Flask, render_template
from dotenv import load_dotenv; load_dotenv()
from .dbmodels import db

def app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.getenv("FLASK_SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite"
    )

    # register blueprints
    from . import auth, account
    app.register_blueprint(auth.bp)
    app.register_blueprint(account.bp)

    # INIT DATABASE
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # END INIT DATABASE

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

    return app