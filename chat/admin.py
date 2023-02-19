from django.contrib import admin
from .models import Message, MessageRoom, UserProfile, FriendRequest, Notification
# Register your models here.

admin.site.register(Message)
admin.site.register(MessageRoom)
admin.site.register(UserProfile)
admin.site.register(FriendRequest)
admin.site.register(Notification)
