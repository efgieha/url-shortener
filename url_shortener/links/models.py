from typing import Any

from django.db import IntegrityError, models, transaction

from url_shortener.links.consts import CODE_LENGTH, CODE_MAX_ATTEMPTS
from url_shortener.links.utils import generate_code


class Link(models.Model):
    short_code = models.CharField(max_length=CODE_LENGTH, unique=True, editable=False)
    long_url = models.URLField(max_length=2048, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.short_code} -> {self.long_url}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.short_code:
            return super().save(*args, **kwargs)
        for _ in range(CODE_MAX_ATTEMPTS):
            self.short_code = generate_code()
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                continue
        raise RuntimeError("Could not generate a unique short code")
