from website.apps.eventbro.models import Event, Convention, EventType


def event(request):
    try:
        convention = Convention.objects.get(active=True, published=True)
        events = Event.objects.filter(convention=convention, published=True)
        events = events.order_by('event_type__name', '-showcase', 'name')

        return {
            'navbar_convention': convention,
            'navbar_events': events,
        }
    except Convention.DoesNotExist:
        # Don't do anything
        return {}