from typing import Iterator
import pandas as pd

from .frame_to_reference import FrameReference
from .column_to_reference import ColumnReference
from .description_frame import DescriptionFrame
from .reference_to_markdown import reference_to_markdown


class GroupReference(FrameReference):

    def __init__(self, iterator: Iterator,
                 description_frame: DescriptionFrame = None):
        super().__init__(pd.DataFrame([]), description_frame)
        [self.append_column_references(i) for i in iterator]

    def append_column_references(self, data):
        self.columns += list(data.columns)
        self.column_references += [
            ColumnReference(data[i], i, self.description_frame)
            for i in data
        ]

    def to_markdown(self, file: str=None):
        result_string = ""
        for description_dictionary in self.get_column_descriptions():
            result_string += reference_to_markdown(**description_dictionary)

        if not file:
            return result_string

        with open(file, "w") as f:
            f.write(result_string)
