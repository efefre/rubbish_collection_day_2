import pytest
from django.urls import reverse
import factories


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
