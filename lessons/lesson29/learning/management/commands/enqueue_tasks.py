import json
import random
from django.core.management.base import BaseCommand
from learning.tasks import multiply


# TASK 09
class Command(BaseCommand):
    help = "Enqueue 50 multiplication tasks with random integer arguments."

    def handle(self, *args, **options):
        submissions = []
        for _ in range(50):
            a, b = random.randint(-20, 20), random.randint(-20, 20)
            task = multiply.delay(a, b)
            submissions.append({"task_id": task.id, "a": a, "b": b})
        self.stdout.write(json.dumps(submissions))
