from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    #Departments within broadcast engineering
    department_name = models.CharField(max_length = 200, unique = True)
    department_head = models.ForeignKey(
        User, null = True, blank = True, 
        on_delete = models.SET_NULL, 
        related_name = 'headed_departments'
    )

    class Meta: 
        ordering = ['department_name']
    
    def __str__(self):
        return self.department_name