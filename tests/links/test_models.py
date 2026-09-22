from unittest.mock import Mock

import pytest

from url_shortener.links import models
from url_shortener.links.consts import CODE_MAX_ATTEMPTS


@pytest.mark.django_db
class TestShortCodeGeneration:
    def test_retries_when_generated_code_is_taken(self, monkeypatch):
        models.Link.objects.create(long_url="https://example.com/some-url", short_code="12345678")
        codes = iter(["12345678", "87654321"])
        monkeypatch.setattr(models, "generate_code", lambda: next(codes))

        new_link = models.Link.objects.create(long_url="https://example.com/some-new-url")

        assert new_link.short_code == "87654321"

    def test_gives_up_after_attempt_limit(self, monkeypatch):
        models.Link.objects.create(long_url="https://example.com/some-url", short_code="12345678")
        mock_generate_code = Mock(return_value="12345678")
        monkeypatch.setattr(models, "generate_code", mock_generate_code)

        with pytest.raises(RuntimeError):
            models.Link.objects.create(long_url="https://example.com/some-new-url")

        assert mock_generate_code.call_count == CODE_MAX_ATTEMPTS
