from __future__ import unicode_literals, absolute_import

import logging

logger = logging.getLogger(__name__)


def salesbro_order_handler(request, order_form, order):
    """
    Finds all passes due to purchased ticket options
    Creates all passes with associated types
    Relate all passes to original order
    Make passes available for registration/assignment
    """
    pass
