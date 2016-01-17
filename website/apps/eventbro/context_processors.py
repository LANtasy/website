from website.apps.eventbro.models import Event, Convention, EventType


def event(request):
    try:
        convention = Convention.objects.get(active=True, published=True)
        event_types = convention.get_event_types()

        return {
            'navbar_convention': convention,
            'navbar_event_types': event_types,
        }
    except Convention.DoesNotExist:
        # Don't do anything
        return {}
