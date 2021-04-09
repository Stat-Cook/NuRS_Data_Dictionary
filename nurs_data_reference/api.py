"""
Easy use APIs
"""
from .reference_spider import ReferenceSpider
from .description_frame import DescriptionFrame
from .group_to_reference import GroupReference


def find_all_columns(path, description_frame: DescriptionFrame = None) -> GroupReference:
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
    GroupReference
    """
    spider = ReferenceSpider(path)
    return spider.to_reference(description_frame)
