from django.contrib import admin

from website.apps.eventbro.models import Convention, Event


class ConventionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'published',),
                ('start', 'end',),
            )
        }),
        ('Details', {
            'fields': ('description',)
        }),
    )

    list_display = ['name', 'start', 'end']

    #list_filter = ("order", "ticket")


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'convention', 'size']

    list_filter = ('name', 'convention',)

admin.site.register(Convention, ConventionAdmin)
admin.site.register(Event, EventAdmin)
