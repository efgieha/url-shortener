from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect

from url_shortener.links.models import Link


def redirect_to_link(request: HttpRequest, short_code: str) -> HttpResponseRedirect:
    """Redirect to the url behind the given short code"""
    link = get_object_or_404(Link, short_code=short_code)
    return redirect(link.long_url)
