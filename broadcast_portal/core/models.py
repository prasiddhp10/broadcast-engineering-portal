from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'), ('UPDATE', 'Update'), ('DELETE', 'Delete'), 
        ('LOGIN', 'Login'), ('LOGOUT', 'Logout'), 
    ]

    user = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    action = models.CharField(max_length = 10, choices = ACTION_CHOICES)
    entity_type = models.CharField(max_length = 60)
    entity_id = models.IntegerField(null = True, blank = True)
    old_value = models.TextField(null = True, blank = True)
    new_value = models.TextField(null = True, blank = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    class Meta: 
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} on {self.entity_type} by {self.user}"