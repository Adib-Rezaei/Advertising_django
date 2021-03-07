from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile

class UserProfileInLine(admin.StackedInline):
    model = UserProfile
    extra = 1

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_staff', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User authentication', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff')}),
    )

    add_fieldsets = (
        ('User authentication', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('permissions', {
            'classes': ('wide',),
            'fields': ('is_admin', 'is_staff'),
        })
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    inlines = [UserProfileInLine,]


admin.site.register(User, UserAdmin)
