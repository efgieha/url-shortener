from django.urls import reverse
from rest_framework import serializers

from url_shortener.links.models import Link


class LinkSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ["short_code", "long_url", "short_url"]
        read_only_fields = ["short_code", "short_url"]

    def get_short_url(self, obj: Link) -> str:
        path = reverse("link-redirect", kwargs={"short_code": obj.short_code})
        request = self.context.get("request")
        return request.build_absolute_uri(path) if request else path
