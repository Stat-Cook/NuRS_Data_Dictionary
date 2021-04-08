"""
Explore the file structure to find excel and csv files nested inside folders.
"""
import os
from typing import Generator
import pandas as pd

from .group_to_reference import GroupReference
from .description_frame import DescriptionFrame


class ReferenceSpider:
    """
    A spider for exploring a file path for all .csv and .xls(x/b) files.
    Parameters
    ----------
    file_path: str
        The initial file path for the spider.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def path_handler(self, path=None) -> Generator:
        """
        Explores the file tree yielding data sets from .csv and .xls(x/b) files.
        Parameters
        ----------
        path: str
            File path to start from.
        Returns
        -------
        Generator
        """
        if not path:
            path = self.file_path
        for i in os.listdir(path):
            file = os.path.join(path, i)

            if ".xls" in i:
                sheets = pd.read_excel(file, sheet_name=None)
                for sheet in sheets:
                    yield sheets[sheet]

            if ".csv" in i:
                yield pd.read_csv(file)

            if os.path.isdir(file):
                for j in self.path_handler(file):
                    yield j

    def to_reference(self, description_frame: DescriptionFrame = None) -> GroupReference:
        """
        Converts the result of the spider to a single GroupReference
        Parameters
        ----------
        description_frame: DescriptionFrame
            A frame containing columns=["Description", "Notes"]

        Returns
        -------
        GroupReference
        """
        return GroupReference(self.path_handler(), description_frame)
