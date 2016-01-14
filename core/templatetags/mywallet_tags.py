from django import template

from api.models import Customer, Biller

register = template.Library()


@register.assignment_tag
def check_customer(user_id):
    return Customer.confirm(user_id)


@register.assignment_tag
def check_biller(user_id):
    return Biller.confirm(user_id)


@register.assignment_tag
def billers():
    return Biller.objects.filter(biller__user__is_active=True)


@register.assignment_tag
def customers():
    return Customer.objects.filter(customer__user__is_active=True)
