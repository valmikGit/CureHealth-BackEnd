from django.contrib import admin
from chatApp_2.models import ChatMessage
# Register your models here.
class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender', 'receiver', 'message', 'is_read']

admin.site.register(ChatMessage, ChatMessageAdmin)