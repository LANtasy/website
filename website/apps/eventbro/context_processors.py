from website.apps.eventbro.models import Event, Convention, EventType


def event(request):
    try:
        convention = Convention.objects.get(active=True, published=True)
        event_types = EventType.objects.filter(event_type_id__convention=convention)
        event_types = event_types.values('name', 'slug').distinct()

        return {
            'navbar_convention': convention,
            'navbar_event_types': event_types,
        }
    except Convention.DoesNotExist:
        # Don't do anything
        return {}
