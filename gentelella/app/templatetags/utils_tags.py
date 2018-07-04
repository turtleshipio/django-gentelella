from django import template

register = template.Library()


@register.filter()
def format_mobile_phone(phone):

    if type(phone) != str:
        return phone

    phone = phone.replace('-', '').replace(' ', '')
    formatted_phone = []

    if len(phone) < 11:
        return phone

    for i, p in enumerate(phone):
        if i != 3 and i != 7:
            formatted_phone.append(p)
        if i == 3 or i == 7:
            formatted_phone.append('-')
            formatted_phone.append(p)
        else:
            continue

    return ''.join(formatted_phone)
