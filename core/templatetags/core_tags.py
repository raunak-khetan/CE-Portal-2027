from django import template

register = template.Library()


@register.filter(name='city_event_date')
def city_event_date(city_event_dates, key):
    """
    Usage in template:
        {% with pair=city_event_dates|city_event_date:city_event_key %}
            {{ pair.event_date|date:'D, d M, Y' }}
        {% endwith %}

    Where city_event_key is a string like "3_7" (city_id_event_id).
    Build this key in template with:
        {% with key=city.id|stringformat:'s'|add:'_'|add:event.id|stringformat:'s' %}
    """
    if not city_event_dates or not key:
        return {}
    return city_event_dates.get(key, {})
