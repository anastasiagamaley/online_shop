from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_joinded')
    list_display_links = ('email', 'first_name')
    # readonly_fields = ('last_login', 'date_joined')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line_1', 'address_line_2', 'city', 'country', 'post_code')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
