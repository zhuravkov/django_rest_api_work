from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Service, WorkType, Firm, Order, OrderInDone, OrderInWork


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




class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'client', 'in_work', 'is_done', 'date')
    class Meta:
        fields = '__all__'


class OrderInWorkAdmin(admin.ModelAdmin):
    list_display = ('order', 'executor', 'date')
    class Meta:
        fields = '__all__'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "order":
            kwargs["queryset"] = Order.objects.filter(in_work=False, is_done=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderInDoneAdmin(admin.ModelAdmin):
    list_display = ('order', 'executor', 'date')
    class Meta:
        fields = '__all__'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "order":
            kwargs["queryset"] = Order.objects.filter(in_work=True, is_done=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Временно
admin.site.register(WorkType)
admin.site.register(Firm)
admin.site.register(Service)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderInWork, OrderInWorkAdmin)
admin.site.register(OrderInDone, OrderInDoneAdmin)



admin.site.register(CustomUser, CustomUserAdmin)

