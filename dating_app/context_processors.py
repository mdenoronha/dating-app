from chat.models import Messages, Winks, Views

def engagement_processor(request):
    # Check this
    if request.user:
        
        new_message = False
        all_messages = Messages.objects.filter(receiver_id=request.user.id)
        for message in all_messages:
            if message.is_read == False:
                new_message = True
                break
            
        new_wink = False
        all_winks = Winks.objects.filter(receiver_id=request.user.id)
        for wink in all_winks:
            if wink.is_read == False:
                new_wink = True
                break
            
        new_view = False
        all_views = Views.objects.filter(receiver_id=request.user.id)
        for view in all_views:
            if view.is_read == False:
                new_view = True
                break
        
        context = {
            'new_message': new_message,
            'new_wink': new_wink,
            'new_view': new_view
        }
    
    return context