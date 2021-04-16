import pytest

from ..nurs_reference_spider import main


@pytest.fixture
def test_data_path():
    return "nurs_data_reference/tests/test_files/spider_folder"


@pytest.fixture
def test_utilities_path():
    return "nurs_data_reference/cli/tests/utilities"


def test_ref_spider(test_data_path):
    main([test_data_path])


def test_ref_spider_with_existing_description(test_data_path, test_utilities_path):
    main([test_data_path, "-dp", f"{test_utilities_path}/description.docx"])


def test_ref_spider_to_new_description(test_data_path, test_utilities_path):
    main([test_data_path, "-dp", f"{test_utilities_path}/description.docx",
          "-new_dp", f"{test_utilities_path}/d2"])
