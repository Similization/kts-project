from urllib import parse


def parse_text(text: str) -> str:
    """
    Returns a string in which all non-ASCII characters are replaced with their '%HH' equivalents.

    :param text: A string to be parsed.
    :type text: str
    :return: The parsed string.
    :rtype: str
    """
    return parse.quote(string=text)
