from django.contrib import admin

from website.apps.eventbro.models import Convention, Event, Registration

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

    # list_filter = ("order", "ticket")


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
    list_display = ('name', 'event_type', 'convention', 'size', 'start', 'end',)

    list_filter = ('name', 'event_type', 'convention',)


class RegistrationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Required', {
            'fields': (
                ('user', 'event',),
                ('date_added',),
            )
        }),
        ('Optional', {
            'fields': (
                ('group_name', 'group_captain',),
                ('game_id',),
            )
        }),
    )

    readonly_fields = ('date_added',)

    list_display = ('id', 'user', 'event', 'date_added', 'game_id', 'group_name', 'group_captain')

    list_filter = ('user', 'event')


admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Convention, ConventionAdmin)
admin.site.register(Event, EventAdmin)
