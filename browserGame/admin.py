from django.contrib import admin
from .models import *

class PaginadorLog(admin.ModelAdmin):
    list_per_page = 25  # cantidad de items por pagina
    list_display= ["typeLog", "user", "message", "created_at"]
# Register your models here.
admin.site.register(User)
admin.site.register(Log, PaginadorLog)
admin.site.register(GlobalOption)
admin.site.register(Action)
admin.site.register(Event)
