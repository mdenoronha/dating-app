from django.contrib import admin
from .models import Profile, ProfileImage
from django.core.mail import send_mass_mail

# # Register your models here.
# class OrderLineAdminInline(admin.TabularInline):
#     model = Profile, ProfileImage
    
# class OrderAdmin(admin.ModelAdmin):
#     inlines = (OrderLineAdminInline, )


def verify(modeladmin, request, queryset):
    queryset.update(is_verified='APPROVED')

    emailtuple = ()
    for value in queryset:
        for query in queryset:
            if isinstance(query, Profile):
                emailtuple = emailtuple + (('Your account has been approved', 'yay!', 'matthewdenoronha@gmail.com', [value.user.email]),)
            else: 
                emailtuple = emailtuple + (('Your profile photo has been approved', 'The following image has been approved: "%s"> '% query.image.url, 'matthewdenoronha@gmail.com', [value.user.email]),)
                
    
             
    send_mass_mail(emailtuple)
    
        
def reject(modeladmin, request, queryset):
    queryset.update(is_verified='NOT APPROVED')
    emailtuple = ()
    
    for value in queryset:
        for query in queryset:
            if isinstance(query, Profile):
                emailtuple = emailtuple + (('Your account has not been approved', 'boo!', 'matthewdenoronha@gmail.com', [value.user.email]),)
            else: 
                emailtuple = emailtuple + (('Your profile photo has been rejected', 'The following image has been rejected: "%s"> '% query.image.url, 'matthewdenoronha@gmail.com', [value.user.email]),)
     
    send_mass_mail(emailtuple)
    
verify.short_description = "Mark selected as verified"
reject.short_description = "Mark selected as rejected"

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'is_verified')
    list_filter = ('is_verified', )
    actions = (verify, reject)
    # list_display_links = ('id', 'title')
    list_per_page = 30
    
admin.site.register(Profile, ProfileAdmin)

class ProfileImageAdmin(admin.ModelAdmin):
    model = ProfileImage
    actions = (verify, reject)
    list_display = ('user', 'image', 'thumbnail', 'is_verified')

    def thumbnail(self, obj):
        return '<img src="{thumb}" width="150" />'.format(thumb=obj.image.url,)
        
    thumbnail.allow_tags = True
    thumbnail.short_description = 'Image'
    
admin.site.register(ProfileImage, ProfileImageAdmin)
