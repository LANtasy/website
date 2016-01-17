from website.apps.eventbro.models import Event, Convention, EventType
from website.apps.salesbro.models import Ticket


def ticket(request):
    try:
        tickets = Ticket.objects.filter(available=True, status=2).count()
        if tickets > 0:
            return {'navbar_tickets': True}
        else:
            return {'navbar_tickets': False}


    except Convention.DoesNotExist:
        # Don't do anything
        return {'navbar_tickets': False}
