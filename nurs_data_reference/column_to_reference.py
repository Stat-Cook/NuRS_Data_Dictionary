"""
Extract reference material for a column of a pandas.DataFrame
"""

from collections import Counter
import pandas as pd

from .description_frame import DescriptionFrame


class ColumnReference:
    """
    Class for converting a column of data to a description
    Parameters
    ----------
    data: pd.Series
        The column of data to process
    column_name: str
        A name to represent the column of data
    description_frame: DescriptionFrame [optional]
        An object holding descriptions and notes on the data
    """

    def __init__(self, data: pd.Series, column_name: str,
                 description_frame: DescriptionFrame = None,
                 source_name=None):

        self.counter = Counter(data.fillna("_nan_"))
        self.column_name = column_name

        if description_frame:
            if column_name not in description_frame.index:
                description_frame.add_rows(column_name)
        self.description_frame = description_frame or \
            DescriptionFrame.blank_from_index([column_name])

        self.description_frame[column_name]["Found In"].update([source_name])

        self.length = data.shape[0]

    def _most_common(self, k: int = 3) -> list:
        """
        Find the most common items in the column, and the number of times they occur.
        Returns a list of the form [(term_1, count_1), (term_2, count_2), ...].
        Parameters
        ----------
        k: int
            the number of items to return.  If there are fewer unique values, the returned
            list is right padded with (None, 0) terms.

        Returns
        -------
        list
        """
        common = self.counter.most_common(k)
        while len(common) < k:
            common += [(None, 0)]
        return common

    def _n_unique(self) -> int:
        """
        Find the number of unique elements
        Returns
        -------
        int
        """
        return len(self.counter.keys())

    def _fetch_descriptions(self):
        if not self.description_frame:
            return {"Descriptions": None, "Notes": None}
        return dict(self.description_frame[self.column_name])

    def description(self, n_most_common=3) -> dict:
        """
        Produce a dictionary to describe the data column.
        Parameters
        ----------
        n_most_common: int
            Number of objects to return in table of common entities.
        Returns
        -------
        dict
        """
        results = {
            "Column_name": self.column_name,
            "N_unique": self._n_unique(),
        }

        div_by = self.length + bool(self.length == 0)

        results.update(dict(zip(
            [f"Common {i}" for i in range(1, 1 + n_most_common)],
            [(i, f"{100*j/div_by:.2f}%") for i, j in self._most_common(n_most_common)]
        )))

        results.update(self._fetch_descriptions())
        return results

    def __repr__(self):
        return f"ColumnReference({self.column_name}, n={self.length}, " \
               f"unique_values={self._n_unique()})"
