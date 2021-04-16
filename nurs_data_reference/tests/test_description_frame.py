import pytest
import pandas as pd
from ..description_frame import DescriptionFrame
from ..exceptions import OverlapException

@pytest.fixture
def test_data_path():
    return "nurs_data_reference/tests/test_files/column_descriptions.xlsx"

@pytest.fixture
def description_frame(test_data_path):
    return DescriptionFrame.blank_from_index(["Col 1", "Col 2"])

@pytest.fixture
def proposed_items():
    return ["Col 1", "Col 3", "Col 4"]

def test_init_from_file(test_data_path):
    frame = DescriptionFrame.from_file(test_data_path)
    assert frame.data.shape[0] == 2


def test_add_rows_unique(description_frame, proposed_items):
    description_frame.add_rows(proposed_items, overlap="unique")
    assert description_frame.data.shape[0] == 4


def test_add_rows_error(description_frame, proposed_items):
    with pytest.raises(OverlapException):
        description_frame.add_rows(proposed_items, overlap="error")


def test_add_rows_force(description_frame, proposed_items):
    description_frame.add_rows(proposed_items, overlap="force")
    assert description_frame.data.shape[0] == 5

