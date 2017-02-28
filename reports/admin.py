from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff', 'imei_numbers')

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
from .models import UsersImei

class ProfileInline(admin.StackedInline):
    model = UsersImei
    can_delete = True
    verbose_name_plural = 'Imei numbers'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)