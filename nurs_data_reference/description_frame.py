import pandas as pd
from typing import Union

from .exceptions import OverlapException


class DescriptionFrame:

    def __init__(self, data: pd.DataFrame):
        self.default_columns = ["Description", "Notes"]
        assert all(i in data.columns for i in self.default_columns)
        self.data = data

    @classmethod
    def from_file(cls, file_path: str, sheet_name=0):
        file_path = file_path
        data = pd.read_excel(file_path, sheet_name=sheet_name)
        return cls(data)

    @classmethod
    def blank_from_index(cls, index):
        data = pd.DataFrame(columns=["Description", "Notes"], index=index)
        return cls(data)

    @classmethod
    def via_concat(cls, frame1: pd.DataFrame, frame2: pd.DataFrame):
        data = pd.concat([frame1, frame2])
        return cls(data)

    def to_excel(self, file_path: str, sheet_name=1):
        self.data.to_excel(file_path, sheet_name=sheet_name)

    def add_rows(self, new_items: Union[list, str], overlap="unique"):
        """
        Update the index of the DescriptionFrame with new value(s).
        Parameters
        ----------
        new_items: Union[str, list]
            either an item to add to the index
             or a list of items to add to the index.
        overlap: str [one of "unique"/ "error"/ "force"]
            method choice for dealing with overlap between 'new_items' and the
            existing index values.
            unique: Add only the values in 'new_items' that are not already in index.
            error: Raise an error if any value in 'new_items' is in index.
            force: force all values in 'new_items' into the index (may cause duplicates)
        """
        assert overlap in ["unique", "error", "force"]
        if isinstance(new_items, str):
            new_items = [new_items]

        overlap_function = self._overlap_functions(overlap)
        new_items = overlap_function(new_items)

        self._force_add_rows(new_items)

    def _overlap_functions(self, key: str):
        overlap_dict = {
            "unique": self._overlap_unique,
            "error": self._overlap_error,
            "force": lambda new_items: new_items
        }
        if key not in overlap_dict:
            raise Exception(f"{key} not one of  \"unique\", \"error\", or \"force\".  "
                            f"Check your code and try again.")
        return overlap_dict[key]

    def _overlap_error(self, new_items):
        overlap = [i for i in new_items if i in self.data.index]
        if overlap:
            raise OverlapException(
                f"Columns already exists in DescriptionFrame ({overlap})"
            )
        return new_items

    def _overlap_unique(self, new_items):
        new_items = [i for i in new_items if i not in self.data.index]
        return new_items

    def _force_add_rows(self, new_items):
        if isinstance(new_items, str):
            new_items = [new_items]

        new_rows = pd.DataFrame(
            columns=self.data.columns,
            index=new_items
        )
        self.data = pd.concat([self.data, new_rows])

    def __getitem__(self, item):
        return self.data.loc[item]

    @property
    def index(self):
        return self.data.index

    @property
    def columns(self):
        return self.data.columns

    @property
    def shape(self):
        return self.data.shape
