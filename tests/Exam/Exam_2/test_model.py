import pytest

from src.Exam.Exam_2.model import *


class Url:
    URL_BEST = "https://xn--80abh7bk0c.xn--p1ai/best/2024"
    URL_RANDOM = "https://xn--80abh7bk0c.xn--p1ai/random"
    URL_NEW = "https://xn--80abh7bk0c.xn--p1ai"


@pytest.mark.parametrize(
    "count,type_qt",
    ((1, Url.URL_BEST), (2, Url.URL_RANDOM), (10, Url.URL_RANDOM), (20, Url.URL_BEST), (25, Url.URL_NEW)),
)
def test_get_qt(count, type_qt):
    new = type_qt == "new"
    type_qt
    result = BashQuotes.req_quotes(type_qt, count=count, new=new)
    assert result != "Error"
