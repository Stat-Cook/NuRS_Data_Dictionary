"""
Easy use APIs
"""
from .reference_spider import ReferenceSpider
from .description_frame import DescriptionFrame


def find_all_columns(path, description_frame: DescriptionFrame = None):
    """
    Explore the folder structure at 'path' for csv and excel files.
    Extracts columns from every data set.
    Parameters
    ----------
    path: str
        Initial file path to search from
    description_frame: DescriptionFrame
        A frame containing columns=["Description", "Notes"]
    Returns
    -------
    GroupedReference
    """
    spider = ReferenceSpider(path)
    return spider.to_reference(description_frame)
