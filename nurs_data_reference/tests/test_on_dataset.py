import pytest
import pandas as pd

from ..column_to_reference import ColumnReference
from ..description_frame import DescriptionFrame


def test_on_dataset():
    dframe = DescriptionFrame.blank_from_index([])
    data = pd.read_csv("nurs_data_reference/tests/test_files/example_data.csv")
    columns = [ColumnReference(data[i], i, dframe) for i in data]
    assert all(i in dframe.index for i in ["Col 1", "Col 2", "Col 3"])
