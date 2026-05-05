from django.db import models
from django.contrib.auth.models import User
from teams.models import Team

# Create your models here.

class MeetingSchedule(models.Model):
    PLATFORM_CHOICES = [
        ('Zoom', 'Zoom'), ('Teams', 'Microsoft Teams'), 
        ('Meet', 'Google Meet'), ('Slack', 'Slack Huddle'),
        ('InPerson', 'In Person')
    ]

    team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name = 'meetings')
    organizer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'organized_meetings')
    title = models.CharField(max_length = 200)
    meeting_link = models.URLField(max_length = 500, blank = True)
    platform = models.CharField(max_length = 50, choices = PLATFORM_CHOICES, blank = True)
    schedule_time = models.DateTimeField()
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['schedule_time']
    
    def __str__(self):
        return f"{self.title} - {self.schedule_time.strftime('%Y-%m-%d %H:%M')}"

class MeetingParticipant(models.Model):
    meeting = models.ForeignKey(
        MeetingSchedule, on_delete = models.CASCADE, related_name = 'participants'
    )
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta: 
        unique_together = ('meeting', 'user')
    
    def __str__(self):
        return f"{self.get_full_name()} in {self.meeting.title}"
