# Utility functions for validating URLs and strings
import re

def is_youtube_url(url: str) -> bool:
    """Verifica se a URL é válida do YouTube / YouTube Music"""
    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be|music\.youtube\.com)/.+$"
    return re.match(pattern, url) is not None


def is_non_empty_string(value: str) -> bool:
    """Verifica se a string não é vazia"""
    return isinstance(value, str) and len(value.strip()) > 0


def is_valid_url(url: str) -> bool:
    """
    Alias para validação de URL.
    Atualmente valida URLs do YouTube / YouTube Music.
    """
    return is_youtube_url(url)