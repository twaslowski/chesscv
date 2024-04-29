import click

from chesscv.util import load_annotations, header
from chesscv.chess import render_fen


@click.command()
@click.option("--image-id", help="Image ID to analyze.")
@click.option("--print-header", is_flag=True, default=False, help="Print header")
def analyze(image_id: str, print_header: bool):
    image_id = int(image_id)
    annotations = load_annotations()
    meta = get_image_meta(image_id, annotations)
    if print_header:
        header(meta)
    image_annotations = get_annotations_for_image(image_id, annotations)
    print(render_fen(image_annotations, meta))


@click.command()
@click.option("--image-name", help="Image name to filter by.")
@click.option("--limit", help="Amount of images to display.", default=5)
def images(image_name: str, limit: int):
    annotations = load_annotations()
    if image_name:
        image_list = [image for image in annotations['images'] if image_name == image['file_name']]
    else:
        image_list = annotations['images'][:limit]
    for image in image_list:
        print(image)


def get_image_meta(image_id: int, annotations: dict) -> dict:
    for image in annotations['images']:
        if image['id'] == image_id:
            return image


def get_annotations_for_image(image_id: int, annotations: dict) -> dict:
    piece_annotations = get_piece_annotations_for_image(image_id, annotations)
    corner_annotations = get_corner_annotations_for_image(image_id, annotations)
    return {
        'pieces': piece_annotations,
        'corners': corner_annotations
    }


def get_piece_annotations_for_image(image_id: int, annotations: dict) -> list[dict]:
    return [annotation for annotation in annotations['annotations']['pieces'] if annotation['image_id'] == image_id]


def get_corner_annotations_for_image(image_id: int, annotations: dict) -> list[dict]:
    return [annotation for annotation in annotations['annotations']['corners'] if annotation['image_id'] == image_id]
