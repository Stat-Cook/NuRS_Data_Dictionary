import argparse


def spider_parser(argv=None) -> argparse.Namespace:
    """
    Implement a command line parser for `nurs_reference_spider`.
    Returns
    -------
    argparse.Namespace
    """
    parser = argparse.ArgumentParser(argv, description='List the content of a folder')

    parser.add_argument('Path', metavar='path', type=str, help='the path to list')

    parser.add_argument(
        "-dp", '--description_path',
        default=None, required=False,
        metavar='description_path', type=str,
        help='path to description doc'
    )

    parser.add_argument(
        "-md", '--markdown_path',
        default="spider", required=False,
        metavar='markdown_path', type=str,
        help='path to write markdown output to'
    )

    parser.add_argument(
        "-new_dp", '--new_description_path',
        default="description", required=False,
        metavar='new_description_path', type=str,
        help='the path to list'
    )

    return parser.parse_args(argv)
