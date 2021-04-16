from .parsers import spider_parser
from ..api import find_all_columns


def main(argv=None):
    args = spider_parser(argv)

    grouped_frame = find_all_columns(args.Path)
    if args.description_path:
        grouped_frame.description_frame.from_word(args.description_path)
    grouped_frame.to_markdown(f"{args.markdown_path}.md")
    grouped_frame.description_frame.to_word(f"{args.new_description_path}.docx")
