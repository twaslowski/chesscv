from util import try_file

ANNOTATIONS_FILE = 'annotations.json'


def main():
    with open(ANNOTATIONS_FILE) as annotations:
        annotations = try_file(ANNOTATIONS_FILE).get()
        # print(annotations.keys())  # ['info', 'images', 'annotations', 'categories', 'splits']
        print(annotations['splits'])


if __name__ == '__main__':
    main()
