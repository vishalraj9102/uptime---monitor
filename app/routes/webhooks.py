from flask import Blueprint, request, jsonify
from app import db
from app.models import Webhook

webhooks_bp = Blueprint('webhooks', __name__)

# Add webhook for Discord notification
@webhooks_bp.route('/', methods=['POST'])
def add_webhook():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Webhook URL is required"}), 400

    webhook = Webhook(url=url)
    db.session.add(webhook)
    db.session.commit()

    return jsonify({"message": "Webhook added successfully", "id": webhook.id}), 201
