from flask import Flask
from extensions import db, scheduler


def create_app():
    """ Application Factory function """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True
    app.config["SCHEDULER_API_ENABLED"] = True

    # register blueprint
    from api import main
    app.register_blueprint(main)

    # initialize extensions
    scheduler.init_app(app)
    db.init_app(app)

    # initialize extensions utilities inside app_context
    with app.app_context():
        from task import get_data_from_web_page
        scheduler.start()
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run()

