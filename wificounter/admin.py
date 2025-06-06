from django.contrib import admin
from .models import Visit

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ip_address', 'user_agent')
    list_filter = ('timestamp',)
    search_fields = ('ip_address', 'user_agent')
    date_hierarchy = 'timestamp'