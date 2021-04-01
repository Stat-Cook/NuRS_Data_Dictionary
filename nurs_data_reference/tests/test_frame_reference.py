import pytest
import pandas as pd

from ..frame_to_reference import FrameReference
from ..description_frame import DescriptionFrame


@pytest.fixture
def example_data():
    return pd.read_csv("nurs_data_reference/tests/test_files/example_data.csv")


@pytest.fixture
def example_frame(example_data):
    return FrameReference(example_data)


@pytest.fixture
def update_description_frame(example_data):
    desc = DescriptionFrame.blank_from_index(["Col 1", "Col 3", "Col 4", "Col 6"])
    desc["Col 1"]["Description"] = "New"
    desc["Col 6"]["Description"] = "New"
    return desc


def test_init(example_data):
    fr = FrameReference(example_data)


def test_descriptions(example_frame):
    results = example_frame.get_column_descriptions()


def test_update_description_frame_replace(example_frame: FrameReference,
                                  update_description_frame: DescriptionFrame):
    example_frame.update_description_frame(update_description_frame, method="replace")
    assert example_frame.description_frame.shape[0] == update_description_frame.shape[0]

def test_update_description_frame_merge(example_frame: FrameReference,
                                  update_description_frame: DescriptionFrame):
    initial_length = example_frame.description_frame.shape[0]
    example_frame.update_description_frame(update_description_frame, method="merge")
    assert example_frame.description_frame.shape[0] == \
           initial_length + update_description_frame.shape[0]

def test_update_description_frame_overwrite(example_frame: FrameReference,
                                  update_description_frame: DescriptionFrame):
    s = set(example_frame.description_frame.index)
    s.update(update_description_frame.index)
    example_frame.update_description_frame(update_description_frame, method="overwrite")
    assert example_frame.description_frame.shape[0] == len(s)
    assert example_frame.description_frame["Col 1"]["Description"] == "New"
    assert example_frame.description_frame["Col 6"]["Description"] == "New"

def test_update_description_frame_add_new(example_frame: FrameReference,
                                  update_description_frame: DescriptionFrame):
    s = set(example_frame.description_frame.index)
    s.update(update_description_frame.index)
    example_frame.update_description_frame(update_description_frame, method="add new only")
    assert example_frame.description_frame.shape[0] == len(s)
    assert example_frame.description_frame["Col 1"]["Description"] != "New"
    assert example_frame.description_frame["Col 6"]["Description"] == "New"
