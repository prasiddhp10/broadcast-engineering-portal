from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from teams.models import Team
from organization.models import Department
from messaging.models import Message
from schedule.models import MeetingSchedule
from .models import AuditLog
from django.utils import timezone
import datetime

# Create your views here.

@login_required
def dashboard(request):
    total_teams = Team.objects.count()
    active_teams = Team.objects.filter(status = 'Active').count()
    offline_teams = Team.objects.exclude(status = 'Active').count()
    total_departments = Department.objects.count()

    #Users team
    user_teams = Team.objects.filter(members__user = request.user).select_related(
        'department', 'team_leader'
    )[:3]

    #unread messages counting
    unread_messages = Message.objects.filter(
        recipient = request.user, status = 'SENT', is_read = False
    ).count(); 

    #upcoming meetings 
    now = timezone.now()
    week_end = now + datetime.timedelta(days = 7)
    upcoming_meetings = MeetingSchedule.objects.filter(schedule_time__gte = now, 
                                                       schedule_time__lte = week_end).filter(organizer = request.user).order_by('schedule_time')[:3]
    recent_activity = AuditLog.objects.select_related('user')[:5]

    context = {
        'total_teams': total_teams, 
        'active_teams': active_teams, 
        'offline_teams': offline_teams, 
        'total_departments' : total_departments, 
        'user_teams': user_teams, 
        'unread_messages': unread_messages, 
        'upcoming_meetings': upcoming_meetings, 
        'recent_activity': recent_activity, 
    }

    return render(request, 'core/dashboard.html', context)