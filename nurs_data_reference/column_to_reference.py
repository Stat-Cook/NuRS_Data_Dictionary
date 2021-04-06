"""
Extract reference material for a column of a pandas.DataFrame
"""
import pandas as pd
from collections import Counter

from .description_frame import DescriptionFrame


class ColumnReference:

    def __init__(self, data: pd.Series, column_name: str,
                 description_frame: DescriptionFrame):

        self.counter = Counter(data.fillna("_nan_"))
        self.column_name = column_name
        if description_frame:
            if column_name not in description_frame.index:
                description_frame.add_rows(column_name)
        self.description_frame = description_frame
        self.n = data.shape[0]

    def _most_common(self, k: int = 3):
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

    def _n_unique(self):
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

    def description(self, n_most_common=3):
        results = {
            "Column_name": self.column_name,
            "N_unique": self._n_unique(),
        }
        results.update(dict(zip(
            [f"Common {i}" for i in range(1, 1 + n_most_common)],
            [(i, f"{100*j/self.n:.2f}%") for i, j in self._most_common(n_most_common)]
        )))
        results.update(self._fetch_descriptions())
        return results
