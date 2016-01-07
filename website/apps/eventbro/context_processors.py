from website.apps.eventbro.models import Event, Convention, EventType


def events_navbar(request):
    conventions = Convention.objects.filter(published=True)
    conventions = conventions.only('name', 'slug', 'start')
    conventions = conventions.order_by('start')

    # events = Event.objects.filter(published=True, convention__published=True)
    # events = events.only('convention', 'event_type', 'name', 'slug', 'start')
    # events = events.order_by('convention__start', 'event_type', 'start', 'name')
    return {
        # 'navbar_events': events,
        'navbar_conventions': conventions,
    }

