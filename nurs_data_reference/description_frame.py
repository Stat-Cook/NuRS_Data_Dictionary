"""
Implement a frame to track the human descriptors and notes on each data column.
"""

from typing import Union
import pandas as pd

from .exceptions import OverlapException, MissingColumnsException
from .frame_to_word import frame_to_word
from .word2reference.read_word import WordReader
from .utilities import string_to_iterable, iterable_to_string


class DescriptionFrame:
    """
    Parameters
    ----------
    data: pandas.DataFrame
        A data frame containing 'Description' and 'Notes' columns.
        Each row is a different column.
    """

    def __init__(self, data: pd.DataFrame, add_columns=False):
        self.default_columns = ["Description", "Notes", "Found In"]
        if not all(i in data.columns for i in self.default_columns):
            if add_columns:
                for i in self.default_columns not in data.columns:
                    data[i] = None
            else:
                raise MissingColumnsException(f"Not all of "
                                              f"{','.join(self.default_columns)} "
                                              f"in supplied Data Frame. ")

        self.data = data
        self._convert_na_to_empty_set()

    @classmethod
    def blank_from_index(cls, index):
        """
        Generate a blank DescriptionFrame from a list of column names.
        Parameters
        ----------
        index: List[str]
            list of column names to use as the index.
        Returns
        -------
        DescriptionFrame
        """
        data = pd.DataFrame(columns=["Description", "Notes",  "Found In"], index=index)
        return cls(data)

    @classmethod
    def via_concat(cls, frame1: pd.DataFrame, frame2: pd.DataFrame):
        """
        Generate a DescriptionFrame by concatenating two data frames.
        Parameters
        ----------
        frame1: pd.DataFrame
            A pandas DataFrame with columns=["Description", "Notes"]
        frame2: pd.DataFrame
            A pandas DataFrame with columns=["Description", "Notes"]
        Returns
        -------
        DescriptionFrame
        """
        data = pd.concat([frame1, frame2])
        return cls(data)

    @classmethod
    def from_file(cls, file_path: str, sheet_name=0):
        """
        Generate DescriptionFrame from excel
        Parameters
        ----------
        file_path: str
            Path to an excel file.
        sheet_name: str [optional]
            The sheet on which the DescriptionFrame is stored.
        Returns
        -------
        DescriptionFrame
        """
        data = pd.read_excel(file_path, sheet_name=sheet_name)
        data["Found In"] = data["Found In"].apply(lambda x: string_to_iterable(x, set))
        return cls(data)


    @classmethod
    def from_word(cls, file: str):
        """
        Generate a DescriptionFrame from word.
        Looks for h2 headings for the index, and h3 headings for the columns.
        Parameters
        ----------
        file: str
            The path to the word file.
        Returns
        -------
        DescriptionFrame
        """
        reader = WordReader(file)
        data = reader.parse_document()
        data = pd.DataFrame(data).T
        return cls(data, True)

    def to_excel(self, file_path: str, sheet_name=1):
        """
        Save the frame to excel format.
        Parameters
        ----------
        file_path: str
            Path to save the file at.
        sheet_name: str [optional]
            Name for the sheet in excel.
        Returns
        -------
        None
        """
        data = self.data
        data["Found In"] = data["Found In"].apply(iterable_to_string)
        self.data.to_excel(file_path, sheet_name=sheet_name)

    def to_word(self, file):
        """
        Save the frame to word - writes each index as:
        index [h2]
        Description [h3]
        ...
        Notes [h3]
        ...
        next_index...
        Parameters
        ----------
        file: str
            file path to write the word doc at.
        Returns
        -------
        None
        """
        data = self.data
        data["Found In"] = data["Found In"].apply(iterable_to_string)
        frame_to_word(self.data, file)

    def add_rows(self, new_items: Union[list, str], overlap="unique") -> None:
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
        self._convert_na_to_empty_set()

    def __getitem__(self, item):
        return self.data.loc[item]

    @property
    def index(self):
        """
        Returns
        -------
        list
        """
        return self.data.index

    @property
    def columns(self):
        """
        Returns
        -------
        list
        """
        return self.data.columns

    @property
    def shape(self):
        """
        Returns
        -------
        tuple
        """
        return self.data.shape

    def _convert_na_to_empty_set(self, column="Found In"):
        nas = self.data[column].isna()
        self.data.loc[nas, column] = self.data.loc[nas, column].apply(lambda x: set())
