import pytest

from src.Exam.Exam_3.wikipedia_race import get_wikipedia_pages


@pytest.mark.parametrize("page_name", ("Mars", "Russia", "Python", "Napoleon", "Main_Page"))
def test_get_page_names(page_name):
    page_names = get_wikipedia_pages(page_name)
    assert len(page_names) > 0
