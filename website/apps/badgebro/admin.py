from django.contrib import admin

# Register your models here.
from website.apps.badgebro.models import Badge


class BadgeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Badge, BadgeAdmin)
