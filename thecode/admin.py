from django.contrib import admin
from .models import Profile, Message, Conversation

# Register your models here.

admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Conversation)
