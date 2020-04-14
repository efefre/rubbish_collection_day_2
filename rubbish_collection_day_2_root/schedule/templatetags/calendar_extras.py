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


@register.simple_tag
def calendar_day(number, month, schedule_dates_for_address):
    polish_holidays_list = polish_holidays(YEAR)

    date_from_calendar = datetime.strptime(
        f"{YEAR}-{month}-{number}", "%Y-%B-%d"
    ).date()
    # ----- HOLIDAYS ----
    if polish_holidays_list.get(date_from_calendar):
        return format_html(f"<span class='holiday'>{number}</span>")
    else:
        # ----- RUBBISH ----
        if schedule_dates_for_address.get(date_from_calendar):
            rubbish_detail = schedule_dates_for_address.get(date_from_calendar)
            if len(rubbish_detail) > 1:
                rubbish_names = ", ".join(
                    rubbish.rubbish_type.name for rubbish in rubbish_detail
                )
                rubbish_marks = "-".join(
                    rubbish.rubbish_type.mark_color for rubbish in rubbish_detail
                )
            else:
                rubbish_names = rubbish_detail[0].rubbish_type.name
                rubbish_marks = rubbish_detail[0].rubbish_type.mark_color
            return format_html(
                f"<span class='mark-rubbish rubbish-{rubbish_marks.replace('#','')}'>{number}</span>"
            )
        else:
            return f"{number}"
