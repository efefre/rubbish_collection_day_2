from django import template
from django.utils.html import format_html
from schedule.models import ScheduleConfiguration
from schedule.utils import polish_holidays
from datetime import datetime
import collections

register = template.Library()


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
    config = ScheduleConfiguration.get_solo()
    year = config.year
    polish_holidays_list = polish_holidays(year)

    date_from_calendar = datetime.strptime(
        f"{year}-{month}-{number}", "%Y-%B-%d"
    ).date()

    # ----- RUBBISH ----
    if schedule_dates_for_address.get(date_from_calendar):
        rubbish_detail = schedule_dates_for_address.get(date_from_calendar)
        if len(rubbish_detail) > 1:
            rubbish_names = ", ".join(
                rubbish.rubbish_type.name for rubbish in rubbish_detail
            )
            rubbish_marks = "-".join(
                sorted([rubbish.rubbish_type.css_name for rubbish in rubbish_detail])
            )
        else:
            rubbish_names = rubbish_detail[0].rubbish_type.name
            rubbish_marks = rubbish_detail[0].rubbish_type.css_name

        # ----- HOLIDAYS ----
        if polish_holidays_list.get(date_from_calendar):
            return format_html(
                f"<span class='sr-only'>{rubbish_names}</span><span class='holiday mark-rubbish {rubbish_marks.replace('#','')}-rubbish' data-toggle='tooltip' data-placement='top' title='{rubbish_names}' data-mark='{date_from_calendar}'>{number}</span>"
            )
        else:
            return format_html(
                f"<span class='sr-only'>{rubbish_names}</span><span class='mark-rubbish {rubbish_marks.replace('#','')}-rubbish' data-toggle='tooltip' data-placement='top' title='{rubbish_names}' data-mark='{date_from_calendar}'>{number}</span>"
            )
    elif polish_holidays_list.get(date_from_calendar):
        return format_html(f"<span class='holiday'>{number}</span>")
    else:
        return format_html(f"<span class='day'>{number}</span>")


@register.simple_tag
def next_year(schedule_dates_for_address):
    config = ScheduleConfiguration.get_solo()
    year = config.year
    next_year_dates = []
    ordered_dates = collections.OrderedDict(sorted(schedule_dates_for_address.items()))

    for date, rubbish_detail in ordered_dates.items():
        date_str = date.strftime("%d-%m-%Y")
        if str(year + 1) in date_str:
            if len(rubbish_detail) > 1:
                rubbish_names = ", ".join(
                    rubbish.rubbish_type.name for rubbish in rubbish_detail
                )
                rubbish_marks = "-".join(
                    sorted(
                        [rubbish.rubbish_type.css_name for rubbish in rubbish_detail]
                    )
                )
            else:
                rubbish_names = rubbish_detail[0].rubbish_type.name
                rubbish_marks = rubbish_detail[0].rubbish_type.css_name

            next_year_dates.append(
                f"<span class='sr-only'>{rubbish_names}</span><span class='mark-rubbish {rubbish_marks.replace('#','')}-rubbish' data-toggle='tooltip' data-placement='top' title='{rubbish_names}' data-mark='{date}'></span>{date}"
            )
    return next_year_dates
