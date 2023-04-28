from django.contrib import admin
from django.core.paginator import Paginator, EmptyPage
from .models import *

class PaginadorLog(admin.ModelAdmin):
    list_per_page = 5  # cantidad de items por pagina

# Register your models here.
admin.site.register(Player)
admin.site.register(UserRol)
admin.site.register(Log, PaginadorLog)
admin.site.register(GlobalOption)
admin.site.register(Action)
admin.site.register(Event)