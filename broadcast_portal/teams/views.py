"""STUDENT 1 – Aamir Ahmed: Teams views"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, TeamDependency, TeamMember, CodeRepo, ContactChannel
from organization.models import Department


@login_required
def team_list(request):
    q = request.GET.get('q', '')
    teams = Team.objects.select_related('department', 'team_leader')
    if q:
        teams = teams.filter(name__icontains=q) | teams.filter(
            department__department_name__icontains=q) | teams.filter(
            team_leader__first_name__icontains=q) | teams.filter(
            team_leader__last_name__icontains=q)
    departments = Department.objects.all()
    dept_filter = request.GET.get('dept', '')
    if dept_filter:
        teams = teams.filter(department__department_name=dept_filter)
    status_filter = request.GET.get('status', '')
    if status_filter:
        teams = teams.filter(status=status_filter)
    view_mode = request.GET.get('view', 'grid')
    return render(request, 'teams/team_list.html', {
        'teams': teams, 'q': q, 'departments': departments,
        'dept_filter': dept_filter, 'status_filter': status_filter,
        'view_mode': view_mode,
    })


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    upstream_deps = TeamDependency.objects.filter(team=team).select_related('depends_on_team')
    downstream_deps = TeamDependency.objects.filter(depends_on_team=team).select_related('team')
    members = TeamMember.objects.filter(team=team).select_related('user')
    repos = CodeRepo.objects.filter(team=team)
    channels = ContactChannel.objects.filter(team=team)
    all_teams = Team.objects.exclude(pk=pk)
    return render(request, 'teams/team_detail.html', {
        'team': team, 'upstream_deps': upstream_deps,
        'downstream_deps': downstream_deps, 'members': members,
        'repos': repos, 'channels': channels,
        'all_teams': all_teams,
    })


@login_required
def dependency_map(request):
    teams = Team.objects.all()
    dependencies = TeamDependency.objects.select_related('team', 'depends_on_team')
    return render(request, 'teams/dependency_map.html', {
        'teams': teams, 'dependencies': dependencies,
    })


@login_required
def email_team(request, pk):
    """Email an entire team – pre-fills compose with the team as recipient."""
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        from messaging.models import Message
        from core.models import AuditLog
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()
        if not subject or not body:
            messages.error(request, 'Subject and message body are required.')
        else:
            msg = Message.objects.create(
                sender=request.user, recipient_team=team,
                subject=subject, body=body, status='SENT',
            )
            AuditLog.objects.create(user=request.user, action='CREATE',
                                    entity_type='Message', entity_id=msg.pk)
            messages.success(request, f'Message sent to {team.name}.')
            return redirect('teams:detail', pk=pk)
    return render(request, 'teams/email_team.html', {'team': team})


@login_required
def add_dependency(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        upstream_id = request.POST.get('upstream_team')
        dep_type = request.POST.get('dependency_type')
        if str(upstream_id) == str(pk):
            messages.error(request, "A team cannot depend on itself.")
        elif TeamDependency.objects.filter(team=team, depends_on_team_id=upstream_id).exists():
            messages.error(request, "This dependency already exists.")
        else:
            upstream = get_object_or_404(Team, pk=upstream_id)
            TeamDependency.objects.create(team=team, depends_on_team=upstream, dependency_type=dep_type)
            messages.success(request, f"Dependency on {upstream.name} added.")
    return redirect('teams:detail', pk=pk)
