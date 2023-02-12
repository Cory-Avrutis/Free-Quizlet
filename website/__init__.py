from flask import Flask

def create_app():
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "Steven_Python_Master"

	# Import Blueprints
	from .auth  import auth
	from .views import views

	# Register blueprint with application
	app.register_blueprint(views, url_prefix="/")
	app.register_blueprint(auth, url_prefix="/")

	return app








