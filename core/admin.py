from django.contrib import admin

from .models import *

admin.site.register(Community)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ParsingQueue)
