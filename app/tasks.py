import requests
from celery import Celery
from app import db
from app.models import Website, Webhook
from datetime import datetime
import logging

# Initialize Celery
celery = Celery()

# Setup basic logging
logging.basicConfig(level=logging.INFO)

@celery.task
def monitor_website(site_id):
    site = Website.query.get(site_id)
    if not site:
        logging.error(f"Site with id {site_id} not found.")
        return

    try:
        # Send GET request to check site status
        response = requests.get(site.url, timeout=10)
        status = "up" if response.status_code == site.expected_status_code else "down"
    except requests.RequestException as e:
        status = "down"
        logging.error(f"Error checking site {site.url}: {e}")

    # Only update if the status has changed
    if status != site.last_status:
        site.last_status = status
        site.last_status_change = datetime.utcnow()  # Update the last status change time
        logging.info(f"Status change detected for site {site.url}: {status}")
        
        # Commit status change to the database
        db.session.commit()

        # Notify webhooks of the status change
        notify_webhooks(site.url, status)

    # Update last_checked for every status check
    site.last_checked = datetime.utcnow()
    db.session.commit()

    # Schedule the next check after the interval
    monitor_website.apply_async((site_id,), countdown=site.check_interval_seconds)


def notify_webhooks(url, status):
    webhooks = Webhook.query.all()
    for webhook in webhooks:
        payload = {"content": f"Website {url} is now {status}"}
        try:
            response = requests.post(webhook.url, json=payload, timeout=10)
            response.raise_for_status()  # Raise error for bad HTTP responses
        except requests.RequestException as e:
            logging.error(f"Error notifying webhook {webhook.url}: {e}")
