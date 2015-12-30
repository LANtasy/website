from django import template

from zebra.conf import options


register = template.Library()

def _set_up_zebra_form(context):
    if not "zebra_form" in context:
        if "form" in context:
            context["zebra_form"] = context["form"]
        else:
            raise Exception, "Missing stripe form."
    context["STRIPE_PUBLISHABLE"] = options.STRIPE_PUBLISHABLE
    return context


@register.inclusion_tag('salesbro/shop/_set_stripe_key.html', takes_context=True)
def salesbro_head_and_stripe_key(context):
    return _set_up_zebra_form(context)
