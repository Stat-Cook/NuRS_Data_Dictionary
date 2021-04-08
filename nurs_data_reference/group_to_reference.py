"""
Extract reference material from every column of a collection of data sets
e.g. every sheet of an excel document.
"""
from typing import Iterator
import pandas as pd

from .frame_to_reference import FrameReference
from .column_to_reference import ColumnReference
from .description_frame import DescriptionFrame


class GroupReference(FrameReference):
    """

    Parameters
    ----------
    iterator: Iterator
        An object that returns multiple pandas.DataFrame objects.
    description_frame: DescriptionFrame
        A frame containing columns=["Description", "Notes"]
    """

    def __init__(self, iterator: Iterator,
                 description_frame: DescriptionFrame = None):
        super().__init__(pd.DataFrame([]), description_frame)
        for i in iterator:
            self.append_column_references(i)

    def append_column_references(self, data) -> None:
        """
        Add ColumnReference objects for the new data set
        Parameters
        ----------
        data: pandas.DataFrame
            The data set with columns to be processed.
        Returns
        -------

        """
        self.columns += list(data.columns)
        self.column_references += [
            ColumnReference(data[i], i, self.description_frame)
            for i in data
        ]
