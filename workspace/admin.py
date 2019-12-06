from django.contrib import admin
from workspace.models import Record,Log,Crawler

# Register your models here.
admin.site.register(Record)
admin.site.register(Log)
admin.site.register(Crawler)
