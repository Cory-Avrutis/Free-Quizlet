from flask import Flask
from flask_login import LoginManager
from .models import User
from .database import *
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Steven_Python_Master"

    # Import Blueprints
    from .auth  import auth
    from .views import views

    # Register blueprint with application
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # registering funcs for templates
    app.jinja_env.globals.update(get_user_privs=get_user_privs)
    # Initialize flasks login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(username):
        if(username_exists(username)):
            return User(username)
        return None

    return app






