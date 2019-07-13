from django.contrib import admin
from .models import Messages, Conversations, Winks, Reject

# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    model = Messages
    list_display = ('sender', 'receiver', 'message_content', 'created_on', 'is_read')
    
class ConversationAdmin(admin.ModelAdmin):
    model = Conversations
    list_display = ('id', )
    
class WinkAdmin(admin.ModelAdmin):
    model = Winks
    list_display = ('sender', 'receiver',  'created_on', 'is_read')
    
class RejectAdmin(admin.ModelAdmin):
    model = Reject
    list_display = ('sender', 'receiver',  'created_on')

admin.site.register(Messages, MessageAdmin)
admin.site.register(Winks, WinkAdmin)
admin.site.register(Conversations, ConversationAdmin)
admin.site.register(Reject, RejectAdmin)