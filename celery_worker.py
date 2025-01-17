from app import create_app, make_celery

# Create the Flask app
app = create_app()

# Create the Celery app
celery = make_celery(app)

if __name__ == "__main__":
    celery.start()
