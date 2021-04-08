"""
Extract reference material from every column of a data set.
"""
import pandas as pd

from .description_frame import DescriptionFrame
from .column_to_reference import ColumnReference
from .reference_to_markdown import reference_to_markdown


class FrameReference:
    """
    Convert all columns in a pandas.DataFrame to ColumnReference objects.
    Parameters
    ----------
    data: pandas.DataFrame
        The data set we wish to analyze
    description_frame: DescriptionFrame
        A frame containing columns=["Description", "Notes"]
    """

    def __init__(self, data: pd.DataFrame, description_frame: DescriptionFrame = None):
        if not description_frame:
            description_frame = DescriptionFrame.blank_from_index(data.columns)
        self.description_frame = description_frame
        self.columns = list(data.columns)

        self.column_references = None
        self.initialize_column_references(data)

    def initialize_column_references(self, data) -> None:
        """
        Initialize the 'column_references' property with the columns in 'data'
        Parameters
        ----------
        data: pandas.DataFrame
            The data set to extract columns from.
        Returns
        -------
        None
        """
        self.column_references = [
            ColumnReference(data[i], i, self.description_frame)
            for i in data
        ]

    def get_column_descriptions(self) -> list:
        """
        Convert the available 'column_references' to descriptions.
        Returns
        -------
        list
        """
        return [i.description() for i in self.column_references]

    def save_description_frame(self, file_path: str, sheet_name: str = 0) -> None:
        """
        Save the description frame to excel.
        Parameters
        ----------
        file_path: str
            Path to excel file
        sheet_name: str [optional]
            Name for the sheet object

        Returns
        -------

        """
        self.description_frame.to_excel(file_path, sheet_name)

    def update_description_frame(self, new_frame: DescriptionFrame, method="replace") -> None:
        """
        Update values stored in the description frame.
        Parameters
        ----------
        new_frame: DescriptionFrame
            A new description frame to merge in.
        method: str ["replace", "merge", "overwrite", "add new only"]
            The type of merge intended:
            * replace - change the existing frame to new_frame
            * merge - concat old and new frames (may cause duplicates)
            * overwrite - concat old and new frame, giving the new frame preference
            * add new only - concat old and new frame, giving the old frame preference

        Returns
        -------
        None
        """
        method_function = {
            "replace": lambda: new_frame,
            "merge": lambda: DescriptionFrame.via_concat(
                self.description_frame.data,
                new_frame.data
            ),
            "overwrite": lambda: self._unique_merge(
                new_frame.data,
                self.description_frame.data
            ),
            "add new only": lambda: self._unique_merge(
                self.description_frame.data,
                new_frame.data
            )
        }
        self.description_frame = method_function[method]()

    def load_description_frame(self, file_path, sheet_name, method: str = "replace") -> None:
        """
        Load a new description frame from file.
        Parameters
        ----------
        file_path: str
            Path to excel file
        sheet_name: str [optional]
            Name for the sheet object
        method: str ["replace", "merge", "overwrite", "add new only"]
            The type of merge intended:
            * replace - change the existing frame to new_frame
            * merge - concat old and new frames (may cause duplicates)
            * overwrite - concat old and new frame, giving the new frame preference
            * add new only - concat old and new frame, giving the old frame preference

        Returns
        -------
        None
        """
        new_frame = DescriptionFrame.from_file(file_path, sheet_name)
        self.update_description_frame(new_frame, method)

    def _unique_merge(self, initial: pd.DataFrame, additional: pd.DataFrame):
        concat_rows = [i for i in additional.index if i not in initial.index]
        return DescriptionFrame.via_concat(initial, additional.loc[concat_rows])

    def to_markdown(self, file: str = None) -> str:
        """
        Convert the
        Parameters
        ----------
        file: str [optional]
            The file path to write the markdown to.
        Returns
        -------
        str
        """
        result_string = ""
        for description_dictionary in self.get_column_descriptions():
            result_string += reference_to_markdown(**description_dictionary)

        if file:
            with open(file, "w") as stream:
                stream.write(result_string)

        return result_string
