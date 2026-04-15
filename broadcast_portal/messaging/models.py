"""
Prasiddha Pant - Student 3 
Features: New message, inbox, sent, draft
"""

from django.db import models
from django.contrib.auth.models import User
from teams.models import Team

# Create your models here.

class Message(models.Model): 
    STATUS_CHOICES = [
        ('SENT', 'Sent'), ('DRAFT', 'Draft'), ('INBOX', 'Inbox')
    ]

    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'sent_messages')
    recipient = models.ForeignKey(
        User, null = True, blank = True, 
        on_delete = models.SET_NULL, related_name = 'received_messages'
    )
    recipient_team = models.ForeignKey(
        Team, null = True, blank = True, 
        on_delete = models.SET_NULL, related_name = 'team_messages'
    )
    subject = models.CharField(max_lenght = 200)
    body = models.TextField()
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'DRAFT')
    is_read = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta: 
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} from {self.sender}"



