from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from app.models import StatusHistory, Website
from app.tasks import monitor_website

sites_bp = Blueprint('sites', __name__)

# Add new site to monitor
@sites_bp.route('/', methods=['POST'])
def add_site():
    data = request.get_json()
    url = data.get('url')
    name = data.get('name')
    check_interval = data.get('check_interval_seconds', 300)
    expected_status_code = data.get('expected_status_code', 200)

    if not url:
        return jsonify({"error": "URL is required"}), 400

    site = Website(url=url, name=name, check_interval_seconds=check_interval, expected_status_code=expected_status_code)
    db.session.add(site)
    db.session.commit()

    # Start monitoring
    monitor_website.delay(site.id)
    return jsonify({"message": "Site added successfully", "id": site.id}), 201

# Remove site from monitoring
@sites_bp.route('/<int:site_id>', methods=['DELETE'])
def remove_site(site_id):
    site = Website.query.get(site_id)
    if not site:
        return jsonify({"error": "Site not found"}), 404

    db.session.delete(site)
    db.session.commit()
    return jsonify({"message": "Site removed successfully"}), 200

# List all monitored sites
@sites_bp.route('/', methods=['GET'])
def get_sites():
    sites = Website.query.all()
    return jsonify([site.to_dict() for site in sites])  # This will now work without error


# Get status history of a site
@sites_bp.route('/<int:site_id>/history', methods=['GET'])
def get_site_history(site_id):
    site = Website.query.get(site_id)
    if not site:
        return jsonify({"error": "Site not found"}), 404

    # Get site status history
    history = site.get_status_history()
    return jsonify(history)


@sites_bp.route('/<int:site_id>/update_status', methods=['POST'])
def update_website_status(site_id):
    site = Website.query.get(site_id)
    if not site:
        return jsonify({"error": "Site not found"}), 404

    # Assume the status comes in the request body
    new_status = request.json.get('status')

    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    # Update the website's last status and time of change
    site.last_status = new_status
    site.last_status_change = datetime.utcnow()
    db.session.commit()

    # Record the status change in the StatusHistory model
    history_entry = StatusHistory(website_id=site.id, status=new_status)
    db.session.add(history_entry)
    db.session.commit()

    return jsonify({"message": "Status updated successfully"}), 200