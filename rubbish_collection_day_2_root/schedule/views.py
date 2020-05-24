import csv
import datetime
import icalendar
from collections import defaultdict


from django.http import HttpResponse
from django.views.generic import FormView, TemplateView

from city_detail.models import Address
from schedule.forms import ChooseAddressForm
from schedule.models import RubbishDistrict, RubbishType
from schedule.models import ScheduleConfiguration
from .utils import days_for_calendar, repl_char, rubbish_combinations


def CONFIG():
    return ScheduleConfiguration.get_solo()


class HomeView(FormView):
    form_class = ChooseAddressForm
    template_name = "schedule/home.html"


# Street - dropdown list option
class LoadStreetView(TemplateView):
    template_name = "schedule/street_dropdown_list_options.html"

    def get_context_data(self, **kwargs):
        city_name = self.request.GET.get("city")
        streets = Address.objects.filter(
                  city__name=city_name).order_by("street")
        context = super().get_context_data(**kwargs)
        context["streets"] = streets
        return context


class CalendarView(TemplateView):
    template_name = "schedule/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_name = self.request.GET.get("city")
        street_name = self.request.GET.get("street")
        address = Address.objects.select_related("city", "street").get(
            city__name=city_name, street__name=street_name
        )
        rubbish_districts = (
            RubbishDistrict.objects.select_related("rubbish_type")
            .prefetch_related("date")
            .filter(addresses=address)
        )
        schedule_dates_for_address = defaultdict(list)

        for district in rubbish_districts:
            for date in district.date.all():
                schedule_dates_for_address[date.date].append(district)

        more_than_5_rubbish_on_same_day = [
            i for i in schedule_dates_for_address.values() if len(i) > 5]
        context["form"] = ChooseAddressForm
        context["calendar"] = days_for_calendar(CONFIG().year)
        context["days_names_list"] = ["Mon", "Tue", "Wed",
                                      "Thu", "Fri", "Sat", "Sun"]
        context["address"] = address
        context["schedule_dates_for_address"] = dict(schedule_dates_for_address)
        context["rubbish_types"] = RubbishType.objects.all()
        context["more_than_5_rubbish_on_same_day"] = more_than_5_rubbish_on_same_day
        return context


class DynamicCssNameView(TemplateView):
    template_name = "schedule/css/mark-rubbish.css"
    content_type = "text/css"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rubbish_type = RubbishType.objects.all()

        rubbish_type_css = []
        for rubbish in rubbish_type:
            rubbish_type_css.append(rubbish.css_name)

        context["rubbish_type_css"] = rubbish_combinations(rubbish_type_css)

        return context


class GenerateSvgView(TemplateView):
    template_name = "schedule/svg/generate-svg.svg"
    content_type = "image/svg+xml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_name = kwargs.get("class_name")

        rubbish_types_details = RubbishType.objects.all()
        rubbish_colors = {}

        for rubbish in rubbish_types_details:
            rubbish_colors[rubbish.css_name] = rubbish.mark_color

        rubbish_types_from_url = (class_name.replace("-rubbish", "")).split("-")

        color_svg = []

        for rubbish in rubbish_types_from_url:
            color_svg.append(rubbish_colors.get(rubbish))

        context["color_svg"] = color_svg
        return context


def ical(request):
    if request.method == "GET":
        city_name = request.GET.get("city")
        street_name = request.GET.get("street")
        address = Address.objects.select_related("city", "street").get(
            city__name=city_name, street__name=street_name
        )
        rubbish_districts = (
            RubbishDistrict.objects.select_related("rubbish_type")
            .prefetch_related("date")
            .filter(addresses=address)
        )

        date_dtstamp = datetime.datetime.utcnow()

        cal = icalendar.Calendar()
        cal.add("prodid", "-//Google Inc//Google Calendar 70.9054//EN")
        cal.add("version", "2.0")
        cal.add("calscale", "gregorian")
        cal.add("method", "publish")
        cal.add("x-wr-timezone", "Europe/Warsaw")

        for district in rubbish_districts:
            for date in district.date.filter(date__gte=date_dtstamp.date()):
                date_dtstart = datetime.datetime.combine(date.date, datetime.time(6, 0))
                date_dtend = datetime.datetime.combine(date.date, datetime.time(7, 0))
                data_description = date.date.strftime("%d-%m-%Y")
                event = icalendar.Event()
                event.add("dtstart", date_dtstart)
                event.add("dtend", date_dtend)
                event.add("dtstamp", date_dtstamp)
                event.add("class", "private")
                event.add(
                    "description",
                    f"{district.rubbish_type.name}: {data_description}. Odpady należy wystawić do godziny 6:00.",
                )
                event.add(
                    "summary",
                    f"Odbiór odpadów: {district.rubbish_type.name} - {data_description}.",
                )
                cal.add_component(event)

        response = HttpResponse(cal.to_ical(), content_type="text/calendar")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="kalendarz-odbioru-odpadow-{repl_char(city_name)}-{repl_char(street_name)}.ics"'
        return response
