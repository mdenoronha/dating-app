from django.contrib import admin
from .models import Messages, Conversations, Winks

# Register your models here.

class MessagesAdmin(admin.ModelAdmin):
    model = Messages
    list_display = ('sender', 'receiver', 'message_content', 'created_on', 'is_read')
    
class ConversationsAdmin(admin.ModelAdmin):
    model = Conversations
    list_display = ('id', )
    
class WinksAdmin(admin.ModelAdmin):
    model = Winks
    list_display = ('sender', 'receiver',  'created_on', 'is_read')

admin.site.register(Messages, MessagesAdmin)
admin.site.register(Winks, WinksAdmin)
admin.site.register(Conversations, ConversationsAdmin)