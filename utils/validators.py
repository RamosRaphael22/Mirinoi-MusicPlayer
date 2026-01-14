# Utility functions for validating URLs and strings
import re

def is_youtube_url(url: str) -> bool:
    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be|music\.youtube\.com)/.+$"
    return re.match(pattern, url) is not None


def is_non_empty_string(value: str) -> bool:
    return isinstance(value, str) and len(value.strip()) > 0


def is_valid_url(url: str) -> bool:
    return is_youtube_url(url)