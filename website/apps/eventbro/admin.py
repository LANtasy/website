from django.contrib import admin
from website.apps.eventbro.models import Convention, Event, Registration, Sponsor, EventType
from sorl.thumbnail.admin import AdminImageMixin
from import_export.admin import ImportExportModelAdmin


class ConventionAdmin(ImportExportModelAdmin):
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

    list_display = ('name', 'start', 'end')
    readonly_fields = ('slug',)


class EventTypeAdmin(ImportExportModelAdmin):
    list_display = ('name', 'overlapping')
    readonly_fields = ('slug', 'uid',)


class EventAdmin(AdminImageMixin, ImportExportModelAdmin):
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
        ('Other Details', {
            'fields': (
                ('sponsor',),
                ('organizer',),
                ('prizes',),
                ('rules',),
            ),
        }),
    )
    list_display = ('name', 'event_type', 'convention', 'size', 'start', 'end',)

    list_filter = ('name', 'event_type', 'convention',)
    readonly_fields = ('slug', )    # 'uid',


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
    list_display = ('id', 'user', 'date_added', 'game_id', 'group_name', 'group_captain') # 'event',
    list_filter = ('user', ) # 'event'


class SponsorAdmin(AdminImageMixin, ImportExportModelAdmin):
    fieldsets = (
        ('Required', {
            'fields': (
                ('name',),
                ('description',),
                ('logo',),
                ('level',),
                ('convention',),
            )
        }),
    )

    list_display = ('name', 'level', 'convention')
    list_filter = ('level', 'convention')
    readonly_fields = ('slug', 'uid')


admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Convention, ConventionAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Sponsor, SponsorAdmin)
