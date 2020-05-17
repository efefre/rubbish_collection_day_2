import pytest
from django.urls import reverse
import factories
from requests_html import HTML


@pytest.fixture(autouse=True)
def reset_factory_boy_sequences():
    factories.StreetFactory.name.reset()


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

        for district in address.rubbish_district.all():
            assert district.date.count() == 2

        url = reverse("schedule:calendar")
        url = f"{url}?city={address.city}&street={address.street}"
        response = (client.get(url)).content

        site = HTML(html=response)
        rubbish_marks = site.find("span.mark-rubbish")
        assert len(rubbish_marks) == 10
