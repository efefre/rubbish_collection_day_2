import csv
import datetime
from collections import defaultdict
from itertools import combinations

from django.http import HttpResponse
from django.views.generic import FormView, TemplateView

from city_detail.models import Address
from schedule.forms import ChooseAddressForm
from schedule.models import RubbishDistrict, RubbishType
from schedule.models import ScheduleConfiguration
from .utils import days_for_calendar, repl_char


CONFIG = ScheduleConfiguration.get_solo()


class HomeView(FormView):
    form_class = ChooseAddressForm
    template_name = "schedule/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["technical_break"] = CONFIG.maintenance_mode
        return context


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

        context["form"] = ChooseAddressForm
        context["year"] = int(CONFIG.year)
        context["calendar"] = days_for_calendar(int(CONFIG.year))
        context["days_names_list"] = ["Mon", "Tue", "Wed",
                                      "Thu", "Fri", "Sat", "Sun"]
        context["address"] = address
        context["schedule_dates_for_address"] = dict(schedule_dates_for_address)
        context["technical_break"] = CONFIG.maintenance_mode
        context["rubbish_types"] = RubbishType.objects.all()
        return context


class DynamicCssNameView(TemplateView):
    template_name = "schedule/css/mark-rubbish.css"
    content_type = "text/css"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rubbish_type = RubbishType.objects.all()

        all_css_combination = []
        rubbish_type_css = []
        for rubbish in rubbish_type:
            rubbish_type_css.append(rubbish.css_name)

        i = 1
        while i <= len(rubbish_type_css):
            rub_combinations = combinations(rubbish_type_css, i)
            for comb in rub_combinations:
                all_css_combination.append(sorted(list(comb)))

            i += 1
        css_names = ["-".join(_) for _ in all_css_combination]

        context["rubbish_type_css"] = css_names

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

        now = datetime.datetime.utcnow()
        date_dtstamp = now.strftime("%Y%m%dT%H%M%SZ")

        response = HttpResponse(content_type="text/calendar")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="kalendarz-odbioru-odpadow-{repl_char(city_name)}-{repl_char(street_name)}.ics"'
        writer = csv.writer(response)
        writer.writerow(["BEGIN:VCALENDAR"])
        writer.writerow(["PRODID:-//Google Inc//Google Calendar 70.9054//EN"])
        writer.writerow(["VERSION:2.0"])
        writer.writerow(["CALSCALE:GREGORIAN"])
        writer.writerow(["METHOD:PUBLISH"])
        writer.writerow(["X-WR-TIMEZONE:Europe/Warsaw"])

        for district in rubbish_districts:
            for date in district.date.all():
                date_dtstart_or_dtend = date.date.strftime("%Y%m%d")
                data_description = date.date.strftime("%d-%m-%Y")
                writer.writerow(["BEGIN:VEVENT"])
                writer.writerow(["DTSTART:{}T060000Z".format(date_dtstart_or_dtend)])
                writer.writerow(["DTEND:{}T070000Z".format(date_dtstart_or_dtend)])
                writer.writerow(["DTSTAMP:{}".format(date_dtstamp)])
                writer.writerow(["CLASS:PRIVATE"])
                writer.writerow(
                    [
                        f"DESCRIPTION:{district.rubbish_type.name}: {data_description}. Odpady należy wystawić do godziny 6:00."
                    ]
                )
                writer.writerow(
                    [
                        f"SUMMARY:Odbiór odpadów: {district.rubbish_type.name} - {data_description}."
                    ]
                )
                writer.writerow(["END:VEVENT"])
        writer.writerow(["END:VCALENDAR"])

        return response
