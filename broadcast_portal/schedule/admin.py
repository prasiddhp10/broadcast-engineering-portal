from django.contrib import admin
from .models import MeetingSchedule, MeetingParticipant

# Register your models here.

admin.site.register(MeetingSchedule)
admin.site.register(MeetingParticipant)
