from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

moment  = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
pagedown = PageDown()
bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    # load config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initial extentions
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # register blueprint
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

    return app
