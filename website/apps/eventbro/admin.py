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
    fieldsets = (
        (None, {
            'fields': (
               ('name', 'convention', 'published',),
               ('description',),
            ),
        }),
        ('Details', {
            'fields': (
                ('size', 'event_type', 'valid_options',),
                ('group_event',),
                ('require_game_id', 'game_id_name',),
            ),
        }),
        ('Image', {
            'fields': (
                ('thumbnail',),
                ('thumb_tag',),
            ),
        }),
        ('Timing', {
            'fields': (
                ('start', 'end',),
            ),
        }),
    )
    list_display = ['name', 'convention', 'size']

    list_filter = ('name', 'convention',)
    readonly_fields = ('thumb_tag',)

admin.site.register(Convention, ConventionAdmin)
admin.site.register(Event, EventAdmin)
