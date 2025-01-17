from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Migrate
from celery import Celery

db = SQLAlchemy()
migrate = Migrate()  # Declare a global Migrate instance
celery = None  # Declare a global Celery instance

def make_celery(app):
    celery_instance = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery_instance.conf.update(app.config)
    return celery_instance

def create_app():
    global celery  # Use the global celery variable

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate

    # Initialize Celery
    celery = make_celery(app)

    # Register Blueprints
    from app.routes.sites import sites_bp
    from app.routes.webhooks import webhooks_bp

    app.register_blueprint(sites_bp, url_prefix="/sites")
    app.register_blueprint(webhooks_bp, url_prefix="/webhooks")

    return app
