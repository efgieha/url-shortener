import secrets
import string

from url_shortener.links.consts import CODE_LENGTH, CODE_MIN_LENGTH


def generate_code(length: int = CODE_LENGTH) -> str:
    """Generate the code based on all letters and digits of certain length"""
    if length < CODE_MIN_LENGTH:
        raise ValueError(f"Code length is lower than {CODE_MIN_LENGTH}")
    return "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
