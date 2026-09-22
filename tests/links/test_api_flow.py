from urllib.parse import urlparse

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestLinkFlow:
    def create(self, apiclient, long_url):
        return apiclient.post(reverse("link-create"), {"long_url": long_url})

    def get(self, apiclient, short_code):
        return apiclient.get(reverse("link-detail", kwargs={"short_code": short_code}))

    def test_created_short_url_redirects_to_long_url(self, apiclient, client):
        long_url = "http://example.com/some-random-code"
        create_response = self.create(apiclient=apiclient, long_url=long_url)

        assert create_response.status_code == status.HTTP_201_CREATED, create_response.data

        short_url = create_response.data["short_url"]
        response = client.get(urlparse(short_url).path)

        assert response.status_code == status.HTTP_302_FOUND
        assert response["Location"] == long_url

    def test_details_return_same_link(self, apiclient):
        long_url = "http://example.com/some-random-code"
        create_response = self.create(apiclient=apiclient, long_url=long_url)
        short_code = create_response.data["short_code"]

        response = self.get(apiclient=apiclient, short_code=short_code)
        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data["long_url"] == long_url
        assert response.data["short_code"] == short_code

    def test_unknown_code_returns_404(self, apiclient, client):
        unknown_code = "TEST1337"

        detail_response = self.get(apiclient=apiclient, short_code=unknown_code)
        assert detail_response.status_code == status.HTTP_404_NOT_FOUND

        redirect_response = client.get(f"/{unknown_code}/")
        assert redirect_response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_long_url_is_rejected(self, apiclient):
        response = self.create(apiclient=apiclient, long_url="invalid-url")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "long_url" in response.data
