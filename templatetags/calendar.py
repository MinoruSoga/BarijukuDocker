import datetime
from django import template
from app.models import Calendar

register = template.Library()


@register.simple_tag
def is_1hour_later(dt, time):
    time = time.split(':')
    later_1hour = datetime.datetime.now() + datetime.timedelta(hours=1)
    target = datetime.datetime.combine(dt, datetime.time(hour=int(time[0]), minute=int(time[1]), second=0))
    return later_1hour <= target

@register.simple_tag
def get_start_time_from_id(id):
    calendar = Calendar.objects.get(id=id)
    start_date = calendar.start_date + datetime.timedelta(hours=9)
    start_time = start_date.strftime('%H:%M')
    return start_time

@register.simple_tag
def get_end_time_from_id(id):
    calendar = Calendar.objects.get(id=id)
    end_date = calendar.end_date + datetime.timedelta(hours=9)
    end_time = end_date.strftime('%H:%M')
    return end_time
