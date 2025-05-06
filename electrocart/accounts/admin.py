from django.contrib import admin
from . models import account
from django.contrib.auth.admin import UserAdmin

class accountadmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_joined','is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_display_links = ('email', 'username')
    ordering = ('-date_joined',)


    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(account, accountadmin)