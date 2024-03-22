
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from greenpot.config import Config
from flask_migrate import Migrate

# ... (other imports)

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
migrate = Migrate()  # Initialize Migrate outside the function

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints and register them
    from greenpot.users.routes import users
    from greenpot.partners.routes import partners
    from greenpot.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(partners)
    app.register_blueprint(main)

    return app


