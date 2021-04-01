import pytest

from ..reference_to_markdown import reference_to_markdown

@pytest.fixture
def ref_dict():
    return {'Column_name': 'Col 1',
            'N_unique': 5, 'Common 1': ('B', '28.00%'), 'Common 2': ('A', '24.00%'),
            'Common 3': ('C', '18.00%'), 'Description': None, 'Notes': None}


def test_ref_to_markdown(ref_dict):
    reference_to_markdown(**ref_dict)
