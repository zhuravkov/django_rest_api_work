from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Service, Work


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Телефон', {'fields': ('phone',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','phone')},
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text')
    class Meta:
        Model = Service

class WorkAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'client_name', 'client_email','in_work', 'client_phone','date')



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Work, WorkAdmin)