import os
import pandas as pd

from .group_to_reference import GroupReference
from .description_frame import DescriptionFrame


class ReferenceSpider:

    def __init__(self, file_path):
        self.file_path = file_path

    def path_handler(self, path=None):
        if not path:
            path = self.file_path
        for i in os.listdir(path):
            file = os.path.join(path, i)

            if ".xls" in i:
                sheets = pd.read_excel(file, sheet_name=None)
                for s in sheets:
                    yield sheets[s]

            if ".csv" in i:
                yield pd.read_csv(file)

            if os.path.isdir(file):
                for i in self.path_handler(file):
                    yield i

    def to_reference(self, description_frame: DescriptionFrame = None):
        return GroupReference(self.path_handler(), description_frame)

