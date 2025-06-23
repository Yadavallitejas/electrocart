from django.contrib import admin
from . models import account, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

class accountadmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_joined','is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_display_links = ('email', 'username')
    ordering = ('-date_joined',)


    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileadmin(admin.ModelAdmin):
    def tumbnail(self, object):
        if object.profile_picture and hasattr(object.profile_picture, 'url'):
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />'.format(object.profile_picture.url))
        else:
            return format_html('<img src="/static/images/avatars/default_avatar.png" style="width: 50px; height: 50px; border-radius: 50%;" />')
    tumbnail.short_description = 'Profile Picture'
    list_display = ('user', 'tumbnail', 'city', 'state', 'country')

# Register your models here.
admin.site.register(account, accountadmin)
admin.site.register(UserProfile, UserProfileadmin)