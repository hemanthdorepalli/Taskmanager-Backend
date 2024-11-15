from django.db import models
from django.contrib.auth.models import User

# Task Model
class Task(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    YET_TO_START = 'yet-to-start'
    IN_PROGRESS = 'in-progress'
    COMPLETED = 'completed'
    HOLD = 'hold'
    STATUS_CHOICES = [
        (YET_TO_START, 'Yet to Start'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (HOLD, 'Hold'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=LOW)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=YET_TO_START)
    deadline = models.DateField()
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
