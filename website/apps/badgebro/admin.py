from django.contrib import admin

# Register your models here.
from website.apps.badgebro.models import Badge, UpgradeTransaction


class BadgeAdmin(admin.ModelAdmin):
    #list_display = product_list_display = ['uid', 'ticket', 'order', 'user']
    list_display = product_list_display = ['uid', 'order', 'user', 'type', 'option', 'network']

    list_filter = ('order', 'ticket')
    readonly_fields = ('uid', )

    search_fields = ['uid', 'network', 'first_name', 'last_name', 'type', 'option']


class UpgradeTransactionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Badge, BadgeAdmin)
admin.site.register(UpgradeTransaction, UpgradeTransactionAdmin)
