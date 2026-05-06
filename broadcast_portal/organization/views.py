from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department
from teams.models import Team, TeamDependency

# Create your views here.

@login_required
def org_chart(request):
    departments = Department.objects.prefetch_related('teams', 'teams__members').all()
    total_teams = Team.objects.count()
    total_members_count = sum(t.members.count() for t in Team.objects.prefetch_related('members'))
    return render(request, 'organization/org_chart.html', {
        'departments': departments, 
        'total_teams': total_teams, 
        'total_members': total_members_count
    })

@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk = pk)
    teams = Team.objects.filter(department = department).prefetch_related('members', 'repos')
    all_deps = TeamDependency.objects.filter(
        team__department = department
    ).select_related('team', 'depends_on_team')
    return render(request, 'organization/department_detail.html', {
        'department': department, 
        'teams': teams, 
        'dependencies': all_deps
    })

@login_required
def team_type_view(request): 
    all_teams = Team.objects.select_related('department', 'team_leader').order_by('team_type', 'name')
    type_map = {}
    for team in all_teams: 
        key = team.team_type.strip() if team.team_type else 'Unclassified'
        type_map.setdefault(key, []).append(team)
        
    return render(request, 'organization/team_type.html', {'type_map': type_map})