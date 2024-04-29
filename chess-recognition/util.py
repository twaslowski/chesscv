import json

from joptional import Optional


def load_annotations() -> dict:
    return read_json('annotations.json').get()


def load_categories() -> dict:
    return read_json('categories.json').get()


def header(meta: dict):
    print(f"Image ID: {meta['id']}")
    print(f"Image Path: {meta['path']}")
    print(f"Move ID: {meta['move_id']}")
    print()


def read_json(path: str) -> Optional[dict] | Optional[None]:
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


def read_image(path: str) -> Optional[bytes] | Optional[None]:
    """
    Returns an Optional[bytes] of the image contents.
    :param path:
    :return:
    """
    try:
        with open(path, 'rb') as file:
            return Optional.of(file.read())
    except FileNotFoundError:
        return Optional.empty()


def pretty_print(d: dict | list):
    print(json.dumps(d, indent=2))
