from urllib import parse


def parse_text(text: str) -> str:
    return parse.quote(string=text)
