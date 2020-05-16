import pytest
from django.urls import reverse
import factories
from requests_html import HTML


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
        alert_box = site.find("div.maintenance-mode", first=True).text
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
