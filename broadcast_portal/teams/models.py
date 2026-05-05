from django.db import models
from django.contrib.auth.models import User
from organization.models import Department

# Create your models here.

class Team(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'), ('DISBANDED', 'Disbanded'), 
        ('MERGED', 'Merged'), ('REFORMED', 'Reformed'),
    ]
    name = models.CharField(max_length = 200, verbose_name= 'Team Name')
    department = models.ForeignKey(
        Department, on_delete  = models.RESTRICT, related_name = 'teams'
    )
    team_leader = models.ForeignKey(
        User, null = True, blank = True, 
        on_delete = models.SET_NULL, related_name = 'led_teams'
    )
    team_type = models.CharField(max_length = 200, blank = True)
    jira_project_name = models.CharField(max_length = 200, blank = True)
    development_focus = models.TextField(blank = True)
    key_skills = models.TextField(blank = True)
    agile_practices = models.CharField(max_length = 200, blank = True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'ACTIVE')
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta: 
        ordering = ['name']
    
    def __str__(self):
        return self.name
    

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name = 'members')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'team_memberships')
    role_in_team = models.CharField(max_length = 120, blank = True)

    class Meta:
        unique_together = ('team', 'user')
    
    def __str__(self):
        return f"{self.user.get_full_name()} in {self.team.name}"

class TeamDependency(models.Model):
    DEPENDENCY_TYPES = [
        ('Infrastructure Support', 'Infrastrucure Support'), 
        ('Bug Resolution', 'Bug Resolution'),
        ('CI/CD Support', 'CI/CD Support'), 
        ('Security Fixes', 'Security Fixes'), 
        ('Agile Coaching', 'Agile Coaching'), 
        ('Other', 'Other'),
    ]
    team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name = 'dependencies')
    depends_on_team = models.ForeignKey(
        Team, on_delete = models.CASCADE, related_name = 'dependents'
    )
    dependency_type = models.CharField(max_length = 50, choices = DEPENDENCY_TYPES, blank = True)

    class Meta:
        unique_together = ('team', 'depends_on_team')
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.team == self.depends_on_team:
            raise ValidationError("A team cannot depend on itself.")
    
    def __str__(self):
        return f"{self.team.name} depends on {self.depends_on_team.name}"

class CodeRepo(models.Model):
    team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name = 'repos')
    repo_name = models.CharField(max_length = 200)
    repo_url = models.URLField(max_length = 2048)

    def __str__(self):
        return self.repo_name
    
class ContactChannel(models.Model):
    CHANNEL_TYPES = [
        ('SLACK', 'Slack'), ('JIRA', 'Jira'), ('STANDUP', 'Daily Standup'), 
        ('WIKI', 'Wiki'), ('EMAIL', 'Email'), 
    ]
    team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name = 'contact_channels')
    channel_type = models.CharField(max_length = 10, choices = CHANNEL_TYPES)
    channel_name = models.CharField(max_length = 200)
    value = models.CharField(max_length = 500)

    def __str__(self):
        return f"{self.channel_type} : {self.channel_name}"