"""Routes for the APIView-based version - no router, paths declared explicitly."""

from django.urls import path

from url_shortener.links.api.views import LinkCreateAPIView, LinkDetailAPIView

urlpatterns = [
    path("", LinkCreateAPIView.as_view(), name="link-create"),
    path("<str:short_code>/", LinkDetailAPIView.as_view(), name="link-detail"),
]
