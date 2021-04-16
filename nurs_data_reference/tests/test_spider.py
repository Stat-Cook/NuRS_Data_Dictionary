import pytest
from ..reference_spider import ReferenceSpider

@pytest.fixture
def spider():
    return ReferenceSpider("nurs_data_reference/tests/test_files/spider_folder")


def test_path_walk(spider: ReferenceSpider):
    files = spider.path_handler()
    assert len([i for i in files]) == 12


def test_spider_group(spider: ReferenceSpider):
    spider_group = spider.to_reference()
    assert len(spider_group.columns) == 132


def test_spider_ref(spider: ReferenceSpider):
    spider_group = spider.to_reference()
    column_descriptions = spider_group.get_column_descriptions()
    assert len(column_descriptions) == 132


def test_spider_ref_to_file(spider: ReferenceSpider):
    spider_group = spider.to_reference()
    spider_group.to_markdown("test_page.txt")


def test_spider_description(spider: ReferenceSpider):
    spider_group = spider.to_reference()
    description = spider_group.description_frame
    result = description["Constant"]["Found In"]
    assert isinstance(result, set)
    assert len(result) == 12


def test_spider_to_word(spider: ReferenceSpider):
    spider_group = spider.to_reference()
    description = spider_group.description_frame
    description.to_word("Spider.docx")
