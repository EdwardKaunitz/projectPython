from django.contrib import admin

# Register your models here.
from .models import Painter, Raiting, Message
admin.site.register(Painter)
admin.site.register(Raiting)
admin.site.register(Message)