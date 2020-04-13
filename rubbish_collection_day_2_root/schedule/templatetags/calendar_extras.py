from django import template
from django.utils.html import format_html
from schedule.models import ScheduleConfiguration
from schedule.utils import polish_holidays
from datetime import datetime

register = template.Library()

config = ScheduleConfiguration.get_solo()
YEAR = int(config.year)


@register.filter
def list_index(list, i):
    return list[int(i)]


@register.filter
def translate_month_to_pl(month):
    months = {
        "January": "Styczeń",
        "February": "Luty",
        "March": "Marzec",
        "April": "Kwiecień",
        "May": "Maj",
        "June": "Czerwiec",
        "July": "Lipiec",
        "August": "Sierpień",
        "September": "Wrzesień",
        "October": "Październik",
        "November": "Listopad",
        "December": "Grudzień",
    }
    return months.get(month)


@register.filter
def translate_day_to_pl(day):
    day_names = {
        "Mon": "Pn",
        "Tue": "Wt",
        "Wed": "Śr",
        "Thu": "Czw",
        "Fri": "Pt",
        "Sat": "Sob",
        "Sun": "Ndz",
    }
    return day_names.get(day)
