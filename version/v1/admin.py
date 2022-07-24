from django.contrib import admin
from .models import Card, User, Transaction
# Register your models here.

class UserAdmin(admin.ModelAdmin):
        list_display = ("email", "full_name")
        fieldsets = (
            (None, {'fields': ('email', 'full_name', 'password')}),
            ('Permissions', {'fields': ('is_superuser', 'last_login')}),
        )
        readonly_fields = ("last_login", "is_superuser")

class CardAdmin(admin.ModelAdmin):
    list_display = ("number", "balance", "date_created")
    readonly_fields = ("number", "cvv", "owner", "balance", "password", "token")

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("code", "from_card", "to_card", "amount", "date")
    readonly_fields = ("code", "from_card", "to_card", "amount", "date")


admin.site.register(User, UserAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Transaction, TransactionAdmin)