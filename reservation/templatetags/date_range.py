from datetime import timedelta
from django import template

register = template.Library()


@register.assignment_tag
def date_range(start_date, end_date):
    """
    A custom tag that generates a list of dates
    from the given `start_date` (inclusive)
    to the given `end_date` (inclusive).
    
    Example Usage:
        {% date_range start_date end_date as date_list %}
        {% for date in date_list %}
            {{ date }}
        {% endfor %}
    :param start_date: A `datetime.date` object.
    :param end_date: A `datetime.date` object. 
    :return: A list of `datetime.date` objects.
    """

    result = []
    current_date = start_date
    while current_date <= end_date:
        result.append(current_date)
        current_date += timedelta(days=1)
    return result
