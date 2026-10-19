from celery import shared_task


# TASK 01
@shared_task
def hello_world():
    """Task 01: this function runs in the Celery worker process."""
    message = "Hello from Celery!"
    print(message, flush=True)
    return message


# TASK 02
# TASK 09
@shared_task
def multiply(a, b):
    """Task 02: receive two numbers and return their product."""
    return a * b


import csv
import random
import time
from datetime import timedelta

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from PIL import Image, ImageChops

from .models import (
    EmailNotification,
    LogEntry,
    ProcessingRecord,
    ScrapedPage,
    UploadedImage,
)


# TASK 03
# TASK 04
@shared_task
def log_timestamp():
    timestamp = timezone.localtime().isoformat()
    with (settings.BASE_DIR / "log.txt").open("a", encoding="utf-8") as output:
        output.write(timestamp + "\n")
    return timestamp


# TASK 05
# TASK 06
@shared_task
def count_users():
    count = get_user_model().objects.count()
    print(f"Users: {count}", flush=True)
    return count


# TASK 07
@shared_task
def update_user_last_login(user_id):
    user = get_user_model().objects.get(pk=user_id)
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])
    return {"user_id": user.pk, "last_login": user.last_login.isoformat()}


# TASK 08
@shared_task
def process_video():
    time.sleep(15)
    return "Przetwarzanie wideo zakończone!"


# TASK 10
# TASK 18
@shared_task
def send_notification(notification_id):
    notification = EmailNotification.objects.get(pk=notification_id)
    time.sleep(2)  # This exercise simulates delivery; no actual email is sent.
    notification.sent_at = timezone.now()
    notification.save(update_fields=["sent_at"])
    return {
        "id": notification.pk,
        "recipient": notification.recipient_email,
        "sent_at": notification.sent_at.isoformat(),
        "queue": "priority_queue",
    }


# TASK 11
@shared_task(bind=True)
def track_progress(self):
    for i in range(1, 101):
        time.sleep(0.1)
        self.update_state(state="PROGRESS", meta={"current": i, "total": 100})
    return {"current": 100, "total": 100}


# TASK 12
@shared_task
def clean_logs():
    cutoff = timezone.now() - timedelta(days=90)
    deleted, _ = LogEntry.objects.filter(created_at__lt=cutoff).delete()
    return {"deleted": deleted, "cutoff": cutoff.isoformat()}


# TASK 13
@shared_task
def scrape_title():
    response = requests.get("https://example.com", timeout=15)
    response.raise_for_status()
    title = BeautifulSoup(response.text, "html.parser").title.get_text(
        strip=True
    )
    page = ScrapedPage.objects.create(url="https://example.com", title=title)
    return {"id": page.pk, "title": title, "url": page.url}


# TASK 14
@shared_task(bind=True)
def generate_csv(self):
    settings.MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    filename = f"users-{self.request.id}.csv"
    with (settings.MEDIA_ROOT / filename).open(
        "w", newline="", encoding="utf-8-sig"
    ) as output:
        writer = csv.writer(output)
        writer.writerow(["username", "email"])
        for user in get_user_model().objects.order_by("pk").iterator():
            # Avoid spreadsheet formula execution when opening exported user input.
            writer.writerow(
                [
                    (
                        ("'" + value)
                        if value.startswith(("=", "+", "-", "@"))
                        else value
                    )
                    for value in (user.username, user.email)
                ]
            )
    return {"filename": filename, "download_url": settings.MEDIA_URL + filename}


# TASK 15
@shared_task(bind=True, max_retries=3)
def retry_connection(self):
    try:
        response = requests.get("https://lesson29.invalid", timeout=5)
        response.raise_for_status()
        return response.status_code
    except requests.RequestException as error:
        raise self.retry(exc=error, countdown=60, max_retries=3)


# TASK 16
@shared_task
def classify_image(image_id):
    record = UploadedImage.objects.get(pk=image_id)
    with Image.open(record.image.path) as image:
        rgb = image.convert("RGB")
        red, green, blue = rgb.split()
        gray = (
            not ImageChops.difference(red, green).getbbox()
            and not ImageChops.difference(green, blue).getbbox()
        )
        result = f"{'grayscale' if gray else 'color'}; {image.width} × {image.height} px"
    record.classification_result = result
    record.save(update_fields=["classification_result"])
    return {
        "id": record.pk,
        "classification": result,
        "image_url": record.image.url,
    }


# TASK 17
@shared_task
def random_number():
    return random.randint(1, 100)


# TASK 17
@shared_task
def times_ten(number):
    return number * 10


# TASK 17
@shared_task(bind=True)
def save_number(self, number):
    filename = f"chain-{self.request.id}.txt"
    settings.MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    (settings.MEDIA_ROOT / filename).write_text(str(number), encoding="utf-8")
    return {"number": number, "download_url": settings.MEDIA_URL + filename}


# TASK 20
@shared_task
def process_record(record_id):
    record = ProcessingRecord.objects.get(pk=record_id)
    record.text = record.text.upper()
    record.processed_at = timezone.now()
    record.save(update_fields=["text", "processed_at"])
    return {
        "id": record.pk,
        "text": record.text,
        "processed_at": record.processed_at.isoformat(),
    }
