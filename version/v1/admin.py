from django.contrib import admin
from django.contrib.auth.models import  User
from .models import Card
# Register your models here.

class UserAdmin(admin.ModelAdmin):
        list_display = ("email", "first_name", "last_name")
        fieldsets = (
            (None, {'fields': ('email', 'first_name', "last_name", 'password')}),
            ('Permissions', {'fields': ('is_superuser', 'last_login')}),
        )

class CardAdmin(admin.ModelAdmin):
    list_display = ("number", "balance", "date_created")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Card, CardAdmin)
