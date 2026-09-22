from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from url_shortener.links.api.serializers import LinkSerializer
from url_shortener.links.models import Link


class LinkCreateAPIView(APIView):
    @extend_schema(request=LinkSerializer, responses={201: LinkSerializer})
    def post(self, request: Request) -> Response:
        serializer = LinkSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LinkDetailAPIView(APIView):
    @extend_schema(responses={200: LinkSerializer})
    def get(self, request: Request, short_code: str) -> Response:
        link = get_object_or_404(Link, short_code=short_code)
        serializer = LinkSerializer(link, context={"request": request})
        return Response(serializer.data)
