from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from website.apps.badgebro.models import Badge


class BadgeAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = product_list_display = ["uid", "ticket", "order", "user"]

    list_filter = ("order", "ticket")
    readonly_fields = ('uid', )

admin.site.register(Badge, BadgeAdmin)
