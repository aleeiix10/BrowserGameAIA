from django.contrib import admin
from .models import *

class GlobalOptionsView(admin.ModelAdmin):
    list_display= ["start_date", "end_date", "last_updated_cron"]

class PaginadorLog(admin.ModelAdmin):
    list_per_page = 25  # cantidad de items por pagina
    list_display= ["typeLog", "user", "message", "created_at"]
    readonly_fields = ["typeLog", "user", "message", "created_at"]
class UserLog(admin.TabularInline):
    model= Log
    extra= 1
    max_num= 5
    readonly_fields = ["typeLog", "user", "message", "created_at"]

class UserEvent(admin.TabularInline):
    model= Event

class UserView(admin.ModelAdmin):
    inlines= [UserLog, UserEvent]
    list_per_page= 25
    list_display= ["username", "current_mana", "level"]

# Register your models here.
admin.site.register(User, UserView)
admin.site.register(Log, PaginadorLog)
admin.site.register(GlobalOption, GlobalOptionsView)
admin.site.register(Action)
admin.site.register(Event)
