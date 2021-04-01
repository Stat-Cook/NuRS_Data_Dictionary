import pandas as pd

from .description_frame import DescriptionFrame
from .column_to_reference import ColumnReference


class FrameReference:

    def __init__(self, data: pd.DataFrame, description_frame: DescriptionFrame = None):
        if not description_frame:
            description_frame = DescriptionFrame.blank_from_index(data.columns)
        self.description_frame = description_frame
        self.columns = list(data.columns)

        self.column_references = None
        self.initialize_column_references(data)

    def initialize_column_references(self, data):
        self.column_references = [
            ColumnReference(data[i], i, self.description_frame)
            for i in data
        ]

    def get_column_descriptions(self):
        return [i.description() for i in self.column_references]

    def save_description_frame(self, file_path, sheet_name):
        self.description_frame.to_excel(file_path, sheet_name)

    def update_description_frame(self, new_frame: DescriptionFrame, method="replace"):
        method_function = {
            "replace": lambda: new_frame,
            "merge": lambda: DescriptionFrame.via_concat(self.description_frame.data, new_frame.data),
            "overwrite": lambda: self._unique_merge(new_frame.data, self.description_frame.data),
            "add new only": lambda: self._unique_merge(self.description_frame.data, new_frame.data)
        }
        self.description_frame = method_function[method]()

    def load_description_frame(self, file_path, sheet_name, method="replace"):
        new_frame = DescriptionFrame.from_file(file_path, sheet_name)
        self.update_description_frame(new_frame, method)

    def _unique_merge(self, initial: pd.DataFrame, additional: pd.DataFrame):
        concat_rows = [i for i in additional.index if i not in initial.index]
        return DescriptionFrame.via_concat(initial, additional.loc[concat_rows])
