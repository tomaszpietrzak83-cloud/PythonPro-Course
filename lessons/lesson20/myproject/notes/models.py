from django.db import models


# --- TASK 06 ---
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
