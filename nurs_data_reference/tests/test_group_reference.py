import pytest
import pandas as pd
import numpy as np

from ..group_to_reference import GroupReference

@pytest.fixture
def data_group():
    return [
        pd.DataFrame({
            "Col 1": np.random.choice(list("ABC"), 50),
            "Col 2": np.random.choice(list("ABBBBC"), 50)
        }),
        pd.DataFrame({
            "Col 3": np.random.choice(list("ABC"), 50),
            "Col 4": np.random.choice(list("ABBBBC"), 50)})
    ]


def test_group_reference(data_group):
    ref = GroupReference(data_group)
    assert len(ref.columns) == 4
    assert len(ref.column_references) == 4


