import pytest
import pandas as pd
import time

from ..column_to_reference import ColumnReference
from ..description_frame import DescriptionFrame


@pytest.fixture
def simple_column():
    return pd.Series(3*["A"]+6*["B"])


@pytest.fixture
def simple_description_frame():
    frm = pd.DataFrame(columns=["Description", "Notes"], index=["Test"])
    return DescriptionFrame(frm)


@pytest.fixture
def nan_frame():
    return pd.DataFrame(index=range(10000), columns=["A", "B"])


@pytest.fixture
def simple_column_reference(simple_column, simple_description_frame):
    return ColumnReference(simple_column, "Test", simple_description_frame)


def test_init(simple_column, simple_description_frame):
    ref = ColumnReference(simple_column, "Test", simple_description_frame)


def test_init_without_description_frame(simple_column):
    ref = ColumnReference(simple_column, "Test", None)


def test_most_common_default_length(simple_column_reference):
    common = simple_column_reference._most_common()
    assert len(common) == 3


def test_most_common_none_default_length(simple_column_reference):
    common = simple_column_reference._most_common(5)
    assert len(common) == 5


def test_n_unique(simple_column_reference):
    n = simple_column_reference._n_unique()
    assert n == 2


def test_description_injection(simple_column, simple_description_frame):
    cr = ColumnReference(simple_column, "Test 2", simple_description_frame)
    assert "Test 2" in cr.description_frame.index
    assert "Test 2" in simple_description_frame.index


def test_nan_column_speed(nan_frame, simple_description_frame):
    t0 = time.time()
    ColumnReference(nan_frame["A"], "Nan_data", simple_description_frame)
    assert (time.time() - t0) < 1
