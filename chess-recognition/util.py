import json

from joptional import Optional


def try_file(path: str) -> Optional[dict] | Optional[None]:
    """
    Returns an Optional[dict] of the file contents.
    :param path:
    :return:
    """
    try:
        with open(path) as file:
            raw = file.read()
            parsed = json.loads(raw)
            return Optional.of(parsed)
    except FileNotFoundError:
        return Optional.empty()
