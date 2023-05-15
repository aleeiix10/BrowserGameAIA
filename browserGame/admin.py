from django.contrib import admin
from .models import *

class GlobalOptionsView(admin.ModelAdmin):
    list_display= ["start_date", "end_date", "last_updated_cron","time_cron_execute_seconds"]

class PaginadorLog(admin.ModelAdmin):
    list_per_page = 25  # cantidad de items por pagina
    list_display= ["typeLog", "user", "message", "created_at"]
    readonly_fields = ["typeLog", "user", "message", "created_at"]

class UserLog(admin.TabularInline):
    model= Log
    extra= 1
    readonly_fields = ["typeLog", "user", "message", "created_at"]

class UserEvent(admin.TabularInline):
    model= Event
    extra= 1
    readonly_fields = ["action", "user", "user_attacked", "timestamp", "success"]
    fk_name='user_attacked'

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserView(BaseUserAdmin):
    inlines = [UserLog, UserEvent]
    list_per_page = 25
    list_display = ["username", "current_life", "experience","current_mana", "level"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("PERSONAL INFO USERS", { 
            "fields": ["level", "current_mana", "current_life", "experience"]
        }),
    )

class EventView(admin.ModelAdmin):
    list_display= ["user", "user_attacked","action", "success","timestamp"]

class ActionView(admin.ModelAdmin):
    list_display= ["name"]

# Register your models here.
admin.site.register(User, UserView)
admin.site.register(Log, PaginadorLog)
admin.site.register(GlobalOption, GlobalOptionsView)
admin.site.register(Action, ActionView)
admin.site.register(Event, EventView)
