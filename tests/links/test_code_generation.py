import string

import pytest

from url_shortener.links.consts import CODE_LENGTH
from url_shortener.links.utils import generate_code


class TestGenerateCode:
    def test_uses_default_length(self):
        assert len(generate_code()) == CODE_LENGTH

    def test_requested_length(self):
        assert len(generate_code(length=12)) == 12

    @pytest.mark.parametrize("length", [4, 0, -1])
    def test_rejects_invalid_length(self, length):
        with pytest.raises(ValueError):
            generate_code(length=length)

    def test_uses_only_letters_and_digits(self):
        allowed_chars = set(string.ascii_letters + string.digits)

        assert set(generate_code(length=100)) <= allowed_chars
