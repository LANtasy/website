from django.contrib import admin

from website.apps.eventbro.models import Convention, Event

from sorl.thumbnail.admin import AdminImageMixin



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


class EventAdmin(AdminImageMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
               ('name',),
               ('convention', 'event_type',),
               ('published',),
               ('start', 'end',),
               ('description',),
            ),
        }),
        ('Details', {
            'fields': (
                ('size',),
                ('valid_options',),
                ('group_event',),
                ('require_game_id', 'game_id_name',),
            ),
        }),
        ('Image', {
            'fields': (
                ('image',),
            ),
        }),
    )
    list_display = ['name', 'convention', 'size']

    list_filter = ('name', 'convention',)

admin.site.register(Convention, ConventionAdmin)
admin.site.register(Event, EventAdmin)
