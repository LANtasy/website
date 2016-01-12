from django.contrib import admin

# Register your models here.
from website.apps.badgebro.models import Badge


class BadgeAdmin(admin.ModelAdmin):
    list_display = product_list_display = ["uid", "ticket", "order", "user"]

    list_filter = ("order", "ticket")
    readonly_fields = ('uid', )

admin.site.register(Badge, BadgeAdmin)
