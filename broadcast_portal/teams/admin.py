from django.contrib import admin
from .models import Team, TeamMember, TeamDependency, CodeRepo, ContactChannel 

# Register your models here.

class TeamMemberInLine(admin.TabularInline):
    model = TeamMember
    extra = 1

class CodeRepoInLiine(admin.TabularInline):
    model = CodeRepo
    extra = 1

class ContactChannelInLine(admin.TabularInline):
    model = ContactChannel 
    extra = 1

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'team_leader', 'status', 'created_at']
    list_filter = ['status', 'department']
    search_fields = ['name', 'team_leader__username']
    inlines = [TeamMemberInLine, CodeRepoInLiine, ContactChannelInLine]

admin.site.register(TeamDependency)