from django import template

register = template.Library()


@register.tag
def get_week(**kwargs):
    start_day = kwargs['start_day']
    end_day = kwargs['end_day']
    weekday = []
    counter = start_day
    if start_day < end_day:
        while counter != end_day + 1:
            weekday.append(counter)
            counter += 1
    else:
        day_index = 6
        while end_day != 0:
            weekday[day_index] = end_day
            end_day -= 1
        temp_index = day_index
        day_index = 0
        while day_index != temp_index:
            weekday[day_index] = start_day
            start_day += 1

    return {'weekdays': weekday}


register.tag('get_week', get_week)