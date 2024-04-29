import os

import click
import cv2

from chesscv.util import load_annotations, header, pretty_print
from chesscv.chess import render_fen
import boto3


@click.command()
@click.option("--image-id", help="Image ID to analyze.", type=click.INT)
@click.option("--print-header", is_flag=True, default=False, help="Print header")
def analyze(image_id: str, print_header: bool):
    """
    Retrieve the annotation data for the given image ID and render the FEN string of the position.
    """
    image_id = int(image_id)
    annotations = load_annotations()
    meta = get_image_meta(image_id, annotations)
    if print_header:
        header(meta)
    image_annotations = get_annotations_for_image(image_id, annotations)
    print(render_fen(image_annotations, meta))


@click.command()
@click.option("--image-name", help="Image name to filter by.")
@click.option("--limit", help="Amount of images to display.", default=5, type=click.INT)
def images(image_name: str, limit: int):
    """
    Retrieve metadata an image by its filename. If no filename is specified, list images.
    """
    annotations = load_annotations()
    if image_name:
        image_list = [
            image for image in annotations["images"] if image_name == image["file_name"]
        ]
    else:
        image_list = annotations["images"][:limit]
    for image in image_list:
        print(image)


@click.command()
@click.option(
    "--image-id",
    help="Image to pre-process and generate training tags for.",
    type=click.INT,
)
def pre_process(image_id: str):
    """
    Pre-process an image and generate training tags.
    """
    image_id = int(image_id)
    annotations = load_annotations()
    image_annotations = get_annotations_for_image(image_id, annotations)
    for piece_annotation in image_annotations["pieces"]:
        del piece_annotation["id"]
        del piece_annotation["image_id"]
    pretty_print(image_annotations)


@click.command()
@click.option("--image-id", help="Image to draw bounding boxes on.", type=click.INT)
def visualize(image_id: str):
    """
    Visualize the bounding boxes of the image.
    """
    image_id = int(image_id)
    annotations = load_annotations()
    meta = get_image_meta(image_id, annotations)
    image_annotations = get_annotations_for_image(image_id, annotations)
    image_path = meta["path"]
    image = cv2.imread(image_path)

    # Iterate over the bounding boxes
    for piece in image_annotations["pieces"]:
        box = piece["bbox"]
        print(box)
        # get coordinates
        x, y, width, height = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        # Draw the bounding box on the image
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
    cv2.imshow("image", image)

    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)

    # closing all open windows
    cv2.destroyAllWindows()


@click.command()
@click.option("--directory", help="Source directory with images")
@click.option("--bucket", help="Target bucket")
def upload(directory: str, bucket: str):
    """
    Upload images to dataset S3 bucket.
    :return:
    """
    s3 = boto3.client("s3")
    for image in os.listdir(directory):
        print(f"Uploading {image}")
        s3.upload_file(f"{directory}/{image}", bucket, image)


def get_image_meta(image_id: int, annotations: dict) -> dict:
    for image in annotations["images"]:
        if image["id"] == image_id:
            return image


def get_annotations_for_image(image_id: int, annotations: dict) -> dict:
    piece_annotations = get_piece_annotations_for_image(image_id, annotations)
    corner_annotations = get_corner_annotations_for_image(image_id, annotations)
    return {"pieces": piece_annotations, "corners": corner_annotations}


def get_piece_annotations_for_image(image_id: int, annotations: dict) -> list[dict]:
    return [
        annotation
        for annotation in annotations["annotations"]["pieces"]
        if annotation["image_id"] == image_id
    ]


def get_corner_annotations_for_image(image_id: int, annotations: dict) -> list[dict]:
    return [
        annotation
        for annotation in annotations["annotations"]["corners"]
        if annotation["image_id"] == image_id
    ]
