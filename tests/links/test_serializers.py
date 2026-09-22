from rest_framework.test import APIRequestFactory

from url_shortener.links.api.serializers import LinkSerializer
from url_shortener.links.models import Link


class TestLinkSerializer:
    def test_short_url_is_absolute_and_ends_with_code(self):
        link = Link(short_code="code1337", long_url="https://example.com/random-page")
        request = APIRequestFactory().get("/")

        data = LinkSerializer(link, context={"request": request}).data

        assert data["short_url"] == "http://testserver/code1337/"

    def test_short_code_from_payload_is_ignored(self):
        serializer = LinkSerializer(data={"long_url": "https://example.com", "short_code": "readOnly"})

        assert serializer.is_valid(), serializer.errors
        assert "short_code" not in serializer.validated_data
