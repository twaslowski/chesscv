from util import load_annotations, header
from chess import render_fen


def main():
    annotations = load_annotations()
    image_id = 102
    meta = get_image_meta(image_id, annotations)
    header(meta)
    image_annotations = get_annotations_for_image(image_id, annotations)
    print(render_fen(image_annotations, meta))


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


if __name__ == '__main__':
    main()
