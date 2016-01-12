from django.contrib import admin
from website.apps.eventbro.forms import DateAdminForm
from website.apps.eventbro.models import Convention, Event, Registration, Sponsor, EventType
from sorl.thumbnail.admin import AdminImageMixin
from import_export.admin import ImportExportModelAdmin


class ConventionAdmin(ImportExportModelAdmin):
    form = DateAdminForm
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'published', 'active',),
                ('start', 'end',),
            )
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Read-Only', {
            'fields': (
                ('slug',),
                ('uid',),
            )
        }),
    )

    list_display = ('slug', 'name', 'published', 'start', 'end',)
    list_filter = ('start',)
    readonly_fields = ('slug', 'uid')


class EventTypeAdmin(ImportExportModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                ('name',),
                ('overlapping',),
            )
        }),
        ('Read-Only', {
            'fields': (
                ('slug',),
                ('uid',),
            )
        }),
    )

    list_display = ('slug', 'name', 'overlapping')
    list_filter = ()
    readonly_fields = ('slug', 'uid',)


class EventAdmin(AdminImageMixin, ImportExportModelAdmin):
    form = DateAdminForm
    fieldsets = (
        (None, {
            'fields': (
               ('name',),
               ('convention', 'event_type',),
               ('published', 'showcase',),
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
        ('Other Details', {
            'fields': (
                ('sponsor',),
                ('organizer',),
                ('prizes',),
                ('rules',),
            ),
        }),
        ('Read-Only', {
            'fields': (
                ('slug',),
                ('uid',),
            )
        }),
    )
    list_display = ('slug', 'published', 'event_type', 'convention', 'size', 'start', 'end',)
    list_filter = ('event_type', 'convention',)
    readonly_fields = ('slug', 'uid',)


class SponsorAdmin(AdminImageMixin, ImportExportModelAdmin):
    fieldsets = (
        ('Required', {
            'fields': (
                ('convention', 'level',),
                ('name',),
                ('url',),
                ('description',),
                ('logo',),
            )
        }),
        ('Read-Only', {
            'fields': (
                ('slug',),
                ('uid',),
            )
        }),
    )

    list_display = ('slug', 'name', 'level', 'convention')
    list_filter = ('level', 'convention')
    readonly_fields = ('slug', 'uid')


class RegistrationAdmin(ImportExportModelAdmin):
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
    list_filter = ('user', 'event',)


admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Convention, ConventionAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Sponsor, SponsorAdmin)
