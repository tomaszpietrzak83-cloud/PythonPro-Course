from django.db import models
from django.utils import timezone


# TASK 10
# TASK 18
class EmailNotification(models.Model):
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)


# TASK 12
class LogEntry(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


# TASK 13
class ScrapedPage(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=500)
    fetched_at = models.DateTimeField(default=timezone.now)


# TASK 16
class UploadedImage(models.Model):
    image = models.ImageField(upload_to="images/")
    classification_result = models.CharField(max_length=250, blank=True)


# TASK 20
class ProcessingRecord(models.Model):
    text = models.CharField(max_length=200)
    processed_at = models.DateTimeField(null=True, blank=True)
