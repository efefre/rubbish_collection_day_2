import pytest
from django.urls import reverse


class TestViewsWithoutLogin:
    @pytest.mark.django_db
    def test_home_view(self, client):
        url = reverse("schedule:home")
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_ajax_load_streets(self, client):
        url = reverse("schedule:ajax_load_streets")
        response = client.get(url)
        assert response.status_code == 200
