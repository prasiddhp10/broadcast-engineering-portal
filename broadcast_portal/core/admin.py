from django.contrib import admin
from .models import AuditLog
# Register your models here.

@admin.register(AuditLog)

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'entity_type', 'entity_id']
    list_filter = ['action', 'entity_type']
    readonly_fields = ['timestamp']