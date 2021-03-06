import pytest
from django.urls import reverse
import factories
import datetime
from requests_html import HTML
from schedule.utils import polish_holidays, rubbish_combinations


@pytest.fixture(autouse=True)
def reset_factory_boy_sequences():
    factories.StreetFactory.name.reset()
    factories.RubbishTypeFactory.name.reset()
    factories.RubbishTypeFactory.mark_color.reset()
    factories.RubbishTypeFactory.css_name.reset()


@pytest.mark.django_db
class TestUrls:
    def test_home_view(self, client):
        url = reverse("schedule:home")
        response = client.get(url)
        assert response.status_code == 200

    def test_ajax_load_streets(self, client):
        url = reverse("schedule:ajax_load_streets")
        response = client.get(url)
        assert response.status_code == 200

    def test_calendar_view(self, client):
        address = factories.AddressFactory()
        url = reverse("schedule:calendar")
        url = f"{url}?city={address.city}&street={address.street}"
        response = client.get(url)
        assert response.status_code == 200

    def test_generate_svg_view(self, client):
        rubbish_district = factories.RubbishDistrictFactory()
        url = reverse(
            "schedule:svg",
            kwargs={"class_name": rubbish_district.rubbish_type.css_name},
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_ical_view(self, client):
        address = factories.AddressFactory()
        url = reverse("schedule:ical_calendar")
        url = f"{url}?city={address.city}&street={address.street}"
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestMaintenanceModeOn:
    def test_home_page_as_user(self, client):
        maintenance_mode = factories.ScheduleConfigurationFactory(maintenance_mode=True)
        response = (client.get(reverse("schedule:home"))).rendered_content

        site = HTML(html=response)
        alert_box = site.find("div.maintenance-mode", first=True).text
        city_label = site.find("#AddressForm > p:nth-child(1) > label", first=True)
        assert (
            alert_box
            == "Przepraszamy. W tej chwili trwa przerwa techniczna.\nZapraszamy później."
        )
        assert city_label is None

    def test_home_page_as_admin(self, admin_client):
        maintenance_mode = factories.ScheduleConfigurationFactory(maintenance_mode=True)
        response = (admin_client.get(reverse("schedule:home"))).rendered_content

        site = HTML(html=response)
        alert_box = site.find("div.maintenance-mode", first=True)
        city_label = site.find("#AddressForm > p:nth-child(1) > label", first=True)
        assert (
            alert_box
            != "Przepraszamy. W tej chwili trwa przerwa techniczna.\nZapraszamy później."
        )
        assert city_label is not None

    def test_calendar_page_as_user(self, client):
        maintenance_mode = factories.ScheduleConfigurationFactory(maintenance_mode=True)
        address = factories.AddressFactory()
        url = reverse("schedule:calendar")
        url = f"{url}?city={address.city}&street={address.street}"
        response = (client.get(url)).content

        site = HTML(html=response)
        alert_box = site.find("div.maintenance-mode", first=True).text
        city_label = site.find("#AddressForm > p:nth-child(1) > label", first=True)
        assert (
            alert_box
            == "Przepraszamy. W tej chwili trwa przerwa techniczna.\nZapraszamy później."
        )
        assert city_label is None

    def test_calendar_page_as_admin(self, admin_client):
        maintenance_mode = factories.ScheduleConfigurationFactory(maintenance_mode=True)
        address = factories.AddressFactory()
        url = reverse("schedule:calendar")
        url = f"{url}?city={address.city}&street={address.street}"
        response = (admin_client.get(url)).content

        site = HTML(html=response)
        alert_box = site.find("div.maintenance-mode", first=True)
        city_label = site.find("#AddressForm > p:nth-child(1) > label", first=True)
        assert (
            alert_box
            != "Przepraszamy. W tej chwili trwa przerwa techniczna.\nZapraszamy później."
        )
        assert city_label is not None


@pytest.mark.django_db
class TestMaintenanceModeOff:
    def test_home_page_as_user(self, client):
        maintenance_mode = factories.ScheduleConfigurationFactory(
            maintenance_mode=False
        )
        response = (client.get(reverse("schedule:home"))).rendered_content

        site = HTML(html=response)
        alert_box = site.find("div.maintenance-mode", first=True)
        city_label = site.find("#AddressForm > p:nth-child(1) > label", first=True)
        assert alert_box is None
        assert city_label is not None

    def test_home_page_as_admin(self, admin_client):
        maintenance_mode = factories.ScheduleConfigurationFactory(
            maintenance_mode=False
        )
        response = (admin_client.get(reverse("schedule:home"))).rendered_content

        site = HTML(html=response)
        alert_box = site.find("div.maintenance-mode", first=True)
        city_label = site.find("#AddressForm > p:nth-child(1) > label", first=True)
        assert alert_box is None
        assert city_label is not None

    def test_calendar_page_as_user(self, client):
        maintenance_mode = factories.ScheduleConfigurationFactory(
            maintenance_mode=False
        )
        address = factories.AddressFactory()
        url = reverse("schedule:calendar")
        url = f"{url}?city={address.city}&street={address.street}"
        response = (client.get(url)).content

        site = HTML(html=response)
        alert_box = site.find("div.maintenance-mode", first=True)
        city_label = site.find("#AddressForm > p:nth-child(1) > label", first=True)
        assert alert_box is None
        assert city_label is not None

    def test_calendar_page_as_admin(self, admin_client):
        maintenance_mode = factories.ScheduleConfigurationFactory(
            maintenance_mode=False
        )
        address = factories.AddressFactory()
        url = reverse("schedule:calendar")
        url = f"{url}?city={address.city}&street={address.street}"
        response = (admin_client.get(url)).content

        site = HTML(html=response)
        alert_box = site.find("div.maintenance-mode", first=True)
        city_label = site.find("#AddressForm > p:nth-child(1) > label", first=True)
        assert alert_box is None
        assert city_label is not None


@pytest.mark.django_db
class TestCalendarView:
    def test_schedule_dates_for_address(self, client):
        date_all_1 = factories.DateFactory()
        date_all_2 = factories.DateFactory()
        district_all = factories.RubbishDistrictFactory.create(
            date=(date_all_1, date_all_2)
        )

        date_bio_1 = factories.DateFactory()
        date_bio_2 = factories.DateFactory()
        district_bio = factories.RubbishDistrictFactory.create(
            date=(date_bio_1, date_bio_2)
        )

        date_rec_1 = factories.DateFactory()
        date_rec_2 = factories.DateFactory()
        district_rec = factories.RubbishDistrictFactory.create(
            date=(date_rec_1, date_rec_2)
        )

        date_ash_1 = factories.DateFactory()
        date_ash_2 = factories.DateFactory()
        district_ash = factories.RubbishDistrictFactory.create(
            date=(date_ash_1, date_ash_2)
        )

        date_big_1 = factories.DateFactory()
        date_big_2 = factories.DateFactory()
        district_big = factories.RubbishDistrictFactory.create(
            date=(date_big_1, date_big_2)
        )

        address = factories.AddressFactory.create(
            rubbish_district=(
                district_all,
                district_ash,
                district_big,
                district_bio,
                district_rec,
            )
        )

        url = reverse("schedule:calendar")
        url = f"{url}?city={address.city}&street={address.street}"
        response = (client.get(url)).content

        site = HTML(html=response)

        all_dates_for_address = set(
            [
                date.date.strftime("%Y-%m-%d")
                for district in address.rubbish_district.all()
                for date in district.date.all()
            ]
        )

        marks = site.find("span.mark-rubbish")
        all_marked_dates = set([mark.attrs.get("data-mark") for mark in marks])

        assert all_dates_for_address == all_marked_dates

    def test_next_year_dates(self, client):
        date_all_1 = factories.DateFactory(date=datetime.date(2021, 1, 4))
        date_all_2 = factories.DateFactory(date=datetime.date(2021, 2, 10))
        district_all = factories.RubbishDistrictFactory.create(
            date=(date_all_1, date_all_2)
        )

        date_bio_1 = factories.DateFactory(date=datetime.date(2021, 1, 7))
        date_bio_2 = factories.DateFactory(date=datetime.date(2021, 2, 12))
        district_bio = factories.RubbishDistrictFactory.create(
            date=(date_bio_1, date_bio_2)
        )

        date_rec_1 = factories.DateFactory(date=datetime.date(2021, 1, 12))
        date_rec_2 = factories.DateFactory(date=datetime.date(2021, 2, 15))
        district_rec = factories.RubbishDistrictFactory.create(
            date=(date_rec_1, date_rec_2)
        )

        date_ash_1 = factories.DateFactory(date=datetime.date(2021, 1, 15))
        date_ash_2 = factories.DateFactory(date=datetime.date(2021, 2, 17))
        district_ash = factories.RubbishDistrictFactory.create(
            date=(date_ash_1, date_ash_2)
        )

        date_big_1 = factories.DateFactory(date=datetime.date(2021, 1, 21))
        date_big_2 = factories.DateFactory(date=datetime.date(2021, 2, 23))
        district_big = factories.RubbishDistrictFactory.create(
            date=(date_big_1, date_big_2)
        )

        address = factories.AddressFactory.create(
            rubbish_district=(
                district_all,
                district_ash,
                district_big,
                district_bio,
                district_rec,
            )
        )

        url = reverse("schedule:calendar")
        url = f"{url}?city={address.city}&street={address.street}"
        response = (client.get(url)).content

        site = HTML(html=response)

        next_year_dates = site.find("div#next-year span.mark-rubbish")
        assert len(next_year_dates) == 10


@pytest.mark.django_db
class TestDynamicCssView:
    def test_class_name(self, client):
        rubbish_type1 = factories.RubbishTypeFactory()
        rubbish_type2 = factories.RubbishTypeFactory()
        rubbish_type3 = factories.RubbishTypeFactory()
        rubbish_type4 = factories.RubbishTypeFactory()
        rubbish_type5 = factories.RubbishTypeFactory()

        url = reverse("schedule:mark-rubbish-css")
        response = (client.get(url)).content

        site = HTML(html=response)

        rubbish_type_css = [
            rubbish_type1.css_name,
            rubbish_type2.css_name,
            rubbish_type3.css_name,
            rubbish_type4.css_name,
            rubbish_type5.css_name,
        ]

        all_rubbish_combinations = rubbish_combinations(rubbish_type_css)

        for css_name in all_rubbish_combinations:
            assert f".{css_name}-rubbish" in site.text

    def test_svg_name_in_css(self, client):
        rubbish_type1 = factories.RubbishTypeFactory()
        rubbish_type2 = factories.RubbishTypeFactory()
        rubbish_type3 = factories.RubbishTypeFactory()
        rubbish_type4 = factories.RubbishTypeFactory()
        rubbish_type5 = factories.RubbishTypeFactory()

        url = reverse("schedule:mark-rubbish-css")
        response = (client.get(url)).content

        site = HTML(html=response)

        rubbish_type_css = [
            rubbish_type1.css_name,
            rubbish_type2.css_name,
            rubbish_type3.css_name,
            rubbish_type4.css_name,
            rubbish_type5.css_name,
        ]

        all_rubbish_combinations = rubbish_combinations(rubbish_type_css)

        for css_name in all_rubbish_combinations:
            assert f"{css_name}-rubbish.svg" in site.text


@pytest.mark.django_db
class TestGenerateSvgView:
    def test_one_color_mark(self, client):
        rubbish_type1 = factories.RubbishTypeFactory()

        url = reverse(
            "schedule:svg", kwargs={"class_name": f"{rubbish_type1.css_name}-rubbish"}
        )

        response = (client.get(url)).content

        site = HTML(html=response)
        assert f"stroke:{rubbish_type1.mark_color}" in site.html

    def test_two_color_mark(self, client):
        rubbish_type1 = factories.RubbishTypeFactory()
        rubbish_type2 = factories.RubbishTypeFactory()

        url = reverse(
            "schedule:svg",
            kwargs={
                "class_name": f"{rubbish_type1.css_name}-{rubbish_type2.css_name}-rubbish"
            },
        )

        response = (client.get(url)).content

        site = HTML(html=response)
        assert f"stroke:{rubbish_type1.mark_color}" in site.html
        assert f"stroke:{rubbish_type2.mark_color}" in site.html

    def test_three_color_mark(self, client):
        rubbish_type1 = factories.RubbishTypeFactory()
        rubbish_type2 = factories.RubbishTypeFactory()
        rubbish_type3 = factories.RubbishTypeFactory()

        url = reverse(
            "schedule:svg",
            kwargs={
                "class_name": f"{rubbish_type1.css_name}-{rubbish_type2.css_name}-{rubbish_type3.css_name}-rubbish"
            },
        )

        response = (client.get(url)).content

        site = HTML(html=response)
        assert f"stroke:{rubbish_type1.mark_color}" in site.html
        assert f"stroke:{rubbish_type2.mark_color}" in site.html
        assert f"stroke:{rubbish_type3.mark_color}" in site.html

    def test_four_color_mark(self, client):
        rubbish_type1 = factories.RubbishTypeFactory()
        rubbish_type2 = factories.RubbishTypeFactory()
        rubbish_type3 = factories.RubbishTypeFactory()
        rubbish_type4 = factories.RubbishTypeFactory()

        url = reverse(
            "schedule:svg",
            kwargs={
                "class_name": f"{rubbish_type1.css_name}-{rubbish_type2.css_name}-{rubbish_type3.css_name}-{rubbish_type4.css_name}-rubbish"
            },
        )

        response = (client.get(url)).content

        site = HTML(html=response)
        assert f"stroke:{rubbish_type1.mark_color}" in site.html
        assert f"stroke:{rubbish_type2.mark_color}" in site.html
        assert f"stroke:{rubbish_type3.mark_color}" in site.html
        assert f"stroke:{rubbish_type4.mark_color}" in site.html

    def test_five_color_mark(self, client):
        rubbish_type1 = factories.RubbishTypeFactory()
        rubbish_type2 = factories.RubbishTypeFactory()
        rubbish_type3 = factories.RubbishTypeFactory()
        rubbish_type4 = factories.RubbishTypeFactory()
        rubbish_type5 = factories.RubbishTypeFactory()

        url = reverse(
            "schedule:svg",
            kwargs={
                "class_name": f"{rubbish_type1.css_name}-{rubbish_type2.css_name}-{rubbish_type3.css_name}-{rubbish_type4.css_name}-{rubbish_type5.css_name}-rubbish"
            },
        )

        response = (client.get(url)).content

        site = HTML(html=response)
        assert f"stroke:{rubbish_type1.mark_color}" in site.html
        assert f"stroke:{rubbish_type2.mark_color}" in site.html
        assert f"stroke:{rubbish_type3.mark_color}" in site.html
        assert f"stroke:{rubbish_type4.mark_color}" in site.html
        assert f"stroke:{rubbish_type5.mark_color}" in site.html

    def test_six_color_mark(self, client):
        rubbish_type1 = factories.RubbishTypeFactory()
        rubbish_type2 = factories.RubbishTypeFactory()
        rubbish_type3 = factories.RubbishTypeFactory()
        rubbish_type4 = factories.RubbishTypeFactory()
        rubbish_type5 = factories.RubbishTypeFactory()
        rubbish_type6 = factories.RubbishTypeFactory(
            name="Test", mark_color="#F1F1F1", css_name="tes"
        )

        url = reverse(
            "schedule:svg",
            kwargs={
                "class_name": f"{rubbish_type1.css_name}-{rubbish_type2.css_name}-{rubbish_type3.css_name}-{rubbish_type4.css_name}-{rubbish_type5.css_name}-{rubbish_type6.css_name}-rubbish"
            },
        )

        response = (client.get(url)).content

        site = HTML(html=response)
        assert f"stroke:{rubbish_type1.mark_color}" not in site.html
        assert f"stroke:{rubbish_type2.mark_color}" not in site.html
        assert f"stroke:{rubbish_type3.mark_color}" not in site.html
        assert f"stroke:{rubbish_type4.mark_color}" not in site.html
        assert f"stroke:{rubbish_type5.mark_color}" not in site.html
        assert (
            f'<text x="210.118px" y="170.646px" style="font-family:\'Arial Black\';font-weight:500;font-size:52px;fill:rgb(255,0,0);">!</text>'
            in site.html
        )


@pytest.mark.django_db
class TestICal:
    def test_dates_in_ical(self, client):
        date_all_1 = factories.DateFactory()
        date_all_2 = factories.DateFactory()
        district_all = factories.RubbishDistrictFactory.create(
            date=(date_all_1, date_all_2)
        )

        date_bio_1 = factories.DateFactory()
        date_bio_2 = factories.DateFactory()
        district_bio = factories.RubbishDistrictFactory.create(
            date=(date_bio_1, date_bio_2)
        )

        date_rec_1 = factories.DateFactory()
        date_rec_2 = factories.DateFactory()
        district_rec = factories.RubbishDistrictFactory.create(
            date=(date_rec_1, date_rec_2)
        )

        date_ash_1 = factories.DateFactory()
        date_ash_2 = factories.DateFactory()
        district_ash = factories.RubbishDistrictFactory.create(
            date=(date_ash_1, date_ash_2)
        )

        date_big_1 = factories.DateFactory()
        date_big_2 = factories.DateFactory()
        district_big = factories.RubbishDistrictFactory.create(
            date=(date_big_1, date_big_2)
        )

        address = factories.AddressFactory.create(
            rubbish_district=(
                district_all,
                district_ash,
                district_big,
                district_bio,
                district_rec,
            )
        )

        now = datetime.datetime.utcnow()
        all_dates_for_address_ical = [
            date.date.strftime("%Y-%m-%d")
            for district in address.rubbish_district.all()
            for date in district.date.filter(date__gte=now.date())
        ]

        url = reverse("schedule:ical_calendar")
        url = f"{url}?city={address.city}&street={address.street}"
        response = (client.get(url)).content

        site = HTML(html=response).text
        begin_vevent = site.count("BEGIN:VEVENT")
        description = site.count("DESCRIPTION:")
        summary = site.count("SUMMARY:")
        end_vevent = site.count("END:VEVENT")

        assert begin_vevent == len(all_dates_for_address_ical)
        assert description == len(all_dates_for_address_ical)
        assert summary == len(all_dates_for_address_ical)
        assert end_vevent == len(all_dates_for_address_ical)
