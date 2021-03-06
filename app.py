from flask import Flask
from extensions import (db,scheduler,marshmallow)
from sqlalchemy_utils.functions import database_exists


def createDB(database_path,database):
    if not database_exists(database_path):
        database.create_all()


def create_app():
    """ Application Factory function """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = False
    app.config["USE_RELOADER"] = False
    app.config["SCHEDULER_API_ENABLED"] = True

    # register blueprint
    from api import main
    app.register_blueprint(main)

    # initialize extensions
    db.init_app(app)
    scheduler.init_app(app)
    marshmallow.init_app(app)


    # initialize extensions utilities inside app_context
    with app.app_context():
        from task import get_data_from_web_page
        createDB(app.config["SQLALCHEMY_DATABASE_URI"] , db)
        scheduler.start()
        
    return app


app = create_app()

if __name__ == "__main__":
    app.run()


