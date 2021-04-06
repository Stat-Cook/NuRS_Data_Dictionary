from .reference_spider import ReferenceSpider
from .description_frame import DescriptionFrame


def find_all_columns(path, description_frame: DescriptionFrame = None):
    spider = ReferenceSpider(path)
    return spider.to_reference(description_frame)
