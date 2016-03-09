from django.contrib import admin

# Register your models here.
from website.apps.badgebro.models import Badge, UpgradeTransaction
from import_export.admin import ExportMixin


class BadgeAdmin(ExportMixin, admin.ModelAdmin):
    #list_display = product_list_display = ['uid', 'ticket', 'order', 'user']
    list_display = product_list_display = ['uid', 'order', 'user', 'type', 'option', 'network']

    list_filter = ('order', 'ticket')
    readonly_fields = ('uid', )

    search_fields = ['uid', 'network', 'first_name', 'last_name', 'type', 'option']


class UpgradeTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'badge', 'old_ticket', 'new_ticket', 'created']


admin.site.register(Badge, BadgeAdmin)
admin.site.register(UpgradeTransaction, UpgradeTransactionAdmin)
