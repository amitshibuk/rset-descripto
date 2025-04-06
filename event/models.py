from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Closed', 'Closed'),
    ]
    
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    organizer = models.CharField(max_length=255)
    max_count = models.PositiveIntegerField()
    in_charge = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    venue = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.name
    
class EventDetails(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    report_details = models.FileField(upload_to='event_reports/', blank=True, null=True)
    feedback_text = models.FileField(upload_to='event_feedbacks/', blank=True, null=True)
    rating = models.FileField(upload_to='event_ratings/', blank=True, null=True)
    participant_count = models.FileField(upload_to='event_participant_counts/', blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return f"Details for {self.event.name}"