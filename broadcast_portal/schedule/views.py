"""STUDENT 4 – Ankit Niroula: Schedule views
Features: Schedule meeting, date/time, platform, message,
          monthly, weekly and upcoming schedules
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import MeetingSchedule, MeetingParticipant
from teams.models import Team
from django.contrib.auth.models import User
from core.models import AuditLog
import datetime
import calendar


@login_required
def schedule_list(request):
    now = timezone.now()

    # All upcoming meetings for this user
    upcoming = MeetingSchedule.objects.filter(schedule_time__gte=now)
    my_meetings = (
        upcoming.filter(organizer=request.user) |
        upcoming.filter(participants__user=request.user)
    ).distinct().order_by('schedule_time')

    # Weekly: next 7 days
    week_end = now + datetime.timedelta(days=7)
    weekly = my_meetings.filter(schedule_time__lte=week_end)

    return render(request, 'schedule/schedule_list.html', {
        'upcoming': my_meetings[:10],
        'weekly': weekly,
        'now': now,
    })


@login_required
def monthly_view(request):
    """Calendar-style monthly view of all meetings."""
    now = timezone.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))

    # Clamp month
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    # All meetings in this month
    month_meetings = MeetingSchedule.objects.filter(
        schedule_time__year=year,
        schedule_time__month=month,
    ).order_by('schedule_time')

    # Build calendar weeks
    cal = calendar.monthcalendar(year, month)

    # Map day -> meetings
    day_meetings = {}
    for meeting in month_meetings:
        day = meeting.schedule_time.day
        day_meetings.setdefault(day, []).append(meeting)

    # Prev / next month
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year

    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    month_name = calendar.month_name[month]

    return render(request, 'schedule/monthly_view.html', {
        'cal': cal,
        'day_meetings': day_meetings,
        'month_name': month_name,
        'month': month,
        'year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': now.day if (now.year == year and now.month == month) else None,
        'total_meetings': month_meetings.count(),
    })


@login_required
def create_meeting(request):
    teams = Team.objects.all()
    users = User.objects.all()
    preselect_team = request.GET.get('team', '')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        team_id = request.POST.get('team')
        platform = request.POST.get('platform', '')
        meeting_link = request.POST.get('meeting_link', '').strip()
        schedule_time = request.POST.get('schedule_time')
        description = request.POST.get('description', '').strip()
        participant_ids = request.POST.getlist('participants')

        if not title or not schedule_time or not team_id:
            messages.error(request, 'Title, team, and schedule time are required.')
            return render(request, 'schedule/create_meeting.html', {
                'teams': teams, 'users': users, 'preselect_team': preselect_team
            })

        meeting = MeetingSchedule.objects.create(
            title=title, team_id=team_id, organizer=request.user,
            platform=platform, meeting_link=meeting_link,
            schedule_time=schedule_time, description=description,
        )
        for uid in participant_ids:
            MeetingParticipant.objects.get_or_create(meeting=meeting, user_id=uid)
        MeetingParticipant.objects.get_or_create(meeting=meeting, user=request.user)

        AuditLog.objects.create(user=request.user, action='CREATE',
                                entity_type='MeetingSchedule', entity_id=meeting.pk)
        messages.success(request, f'Meeting "{title}" scheduled successfully.')
        return redirect('schedule:list')

    return render(request, 'schedule/create_meeting.html', {
        'teams': teams, 'users': users, 'preselect_team': preselect_team,
    })


@login_required
def meeting_detail(request, pk):
    meeting = get_object_or_404(MeetingSchedule, pk=pk)
    participants = MeetingParticipant.objects.filter(meeting=meeting).select_related('user')
    return render(request, 'schedule/meeting_detail.html', {
        'meeting': meeting, 'participants': participants,
    })
