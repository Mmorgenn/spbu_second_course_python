import pytest

from src.Exam.Exam_3.wiki_race import *


@pytest.mark.parametrize("page", ("Cheese", "China", "Russia", "Tree", "March"))
def test_get_pages(page):
    assert len(get_wikipedia_pages(page)) > 0


@pytest.mark.parametrize(
    "node,path",
    (
        (Node("Dada", None), ["Dada"]),
        (Node("Math", Node("Physic", None)), ["Physic", "Math"]),
        (Node("Foo", Node("Boo", Node("Goo", None))), ["Goo", "Boo", "Foo"]),
    ),
)
def test_get_path(node, path):
    assert node.get_path() == path


@pytest.mark.parametrize(
    "list_pages, expected",
    (
        (["Toilet", "Skibidi_Toilet", "Donald_Trump", "Adolf_Hitler"], 5),
        (["Toilet"], 0),
        (["Cheese", "Cheese"], 1),
        (["Car", "China", "Computer"], 5),
    ),
)
def test_wiki_race(list_pages, expected):
    assert len(get_wiki_path(list_pages, 8, False)) == expected
