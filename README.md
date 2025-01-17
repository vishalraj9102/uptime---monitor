---

# Uptime Monitor with Discord Notifications 🚀

## Overview

The **Uptime Monitor** service tracks the availability of websites and sends real-time notifications via Discord webhooks when a site goes down or recovers. It helps to monitor websites and ensures uptime with automated checks.

---

## Features ✨

- **Website Monitoring**: Monitor websites for uptime and downtime.
- **Discord Notifications**: Receive alerts when a website goes down or recovers.
- **Background Task**: Continuously monitor websites in the background using Celery or asyncio.
- **API Endpoints**:
  - Add/remove websites to monitor
  - Get monitoring status for websites
  - Configure Discord webhook for notifications
- **Data Persistence**: Store site status history in **PostgreSQL**.
- **Error Handling**: Handles invalid URLs, network timeouts, and Discord webhook failures.
- **Authentication (Optional)**: API authentication for secure access.

---

## Table of Contents 📚

- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Testing](#testing)
- [License](#license)

---

## Installation 🛠

To get started with this project, follow these steps:

### Prerequisites

1. **Python 3.11+**: Install the latest version of Python.
2. **Docker & Docker Compose**: For containerization (optional but recommended).
3. **PostgreSQL**: For data storage.

### Steps to Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-repo/uptime-monitor.git
    cd uptime-monitor
    ```

2. **Create a virtual environment and install dependencies**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Set up PostgreSQL**:

   You can use a PostgreSQL service via Docker or install it locally.

   - Docker setup:
     ```yaml
     version: '3.8'

     services:
       postgres:
         image: postgres:latest
         container_name: postgres
         environment:
           POSTGRES_DB: uptime_monitor
           POSTGRES_USER: user
           POSTGRES_PASSWORD: password
         ports:
           - "5432:5432"
     ```

4. **Start the application**:

    Run the app with Docker Compose:

    ```bash
    docker-compose up --build
    ```

---

## API Endpoints ⚡️

### `POST /sites` - Add a new site to monitor

#### Request Body:
```json
{
    "url": "https://example.com",
    "check_interval_seconds": 300,
    "name": "My Website",
    "expected_status_code": 200
}
```

#### Response:
```json
{
    "id": 1,
    "url": "https://example.com",
    "status": "up",
    "response_time_ms": 123,
    "last_checked": "2024-01-16T20:00:00Z",
    "last_status_change": "2024-01-16T19:00:00Z"
}
```

### `DELETE /sites/{id}` - Remove a site from monitoring

### `GET /sites` - List all monitored sites

### `GET /sites/{id}/history` - Get status history of a site

### `POST /webhook` - Configure Discord webhook

#### Request Body:
```json
{
    "webhook_url": "https://discord.com/api/webhooks/your-webhook-id"
}
```

---

## Background Task 🕐

### Celery for Background Monitoring

Use **Celery** to perform the monitoring task in the background. The worker will check each website at the specified interval.

- **Celery Setup**:

    - **Task**: Check the website's status and send a notification to the configured Discord webhook if the status changes.
    - **Database**: Store status history in PostgreSQL.

---

## Discord Integration 💬

Set up a **Discord webhook URL** to receive notifications when:

- A site becomes unreachable.
- A site recovers.
- First failed attempt after success.
- First successful attempt after failure.

**Configure Discord Webhook** via the `/webhook` endpoint.

---

## Testing 🧪

### Core Monitoring Logic

You can test core monitoring logic using **pytest**.

Example of testing Discord notifications:

```python
import pytest
from unittest.mock import patch
from app import notify_discord

@pytest.mark.asyncio
async def test_discord_notification():
    with patch('app.notify_discord.send') as mock_send:
        await notify_discord("Site is down", "https://discord.com/api/webhooks/your-webhook-id")
        mock_send.assert_called_once()
```

---

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Technologies Used 💻

- **Python 3.11+**
- **Flask** for API
- **Celery** for background tasks
- **PostgreSQL** for data persistence
- **Docker** for containerization
- **Discord Webhooks** for notifications

---
