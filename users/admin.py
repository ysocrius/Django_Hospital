from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address


class AddressInline(admin.StackedInline):
    model = Address
    can_delete = False


class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser model"""
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profile_picture')}),
        ('Address', {'fields': ('address_line1', 'city', 'state', 'pincode')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 
                      'profile_picture', 'user_type', 'address_line1', 'city', 'state', 'pincode',
                      'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
