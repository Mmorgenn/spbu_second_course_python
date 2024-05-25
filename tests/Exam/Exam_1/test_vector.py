import pytest

from src.Exam.Exam_1.vector import ArityError, Vector


@pytest.mark.parametrize(
    "elements,size", (([0], 1), ([], 0), ([1, 1, 1], 3), ([1, 2, 3, 4, 5], 5), ([2, 2, 2, 2, 2, 3, 5], 7))
)
def test_size(elements, size):
    assert len(Vector(elements)) == size


@pytest.mark.parametrize(
    "elements_1,elements_2,expected",
    (
        ([], [], True),
        ([1], [], False),
        ([1, 2, 3], [1, 2, 3], True),
        ([4, 5, 6], [5, 4, 6], False),
        ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0], True),
        ([1], [2], False),
        ([1.23, 4.1], [1.23, 4.1], True),
    ),
)
def test_eq(elements_1, elements_2, expected):
    assert (Vector(elements_1) == Vector(elements_2)) == expected


@pytest.mark.parametrize(
    "elements,expected",
    (
        ([], True),
        ([0], True),
        ([0, 0, 0, 0, 0], True),
        ([0.0, 0.0, 0.0], True),
        ([1], False),
        ([0, 0, 0, 0, 1], False),
        ([1, 0, 0, 2, 3], False),
        ([0, 2, 2, 2], False),
    ),
)
def test_is_null(elements, expected):
    assert Vector(elements).is_null() == expected


@pytest.mark.parametrize(
    "elements_1,elements_2,expected",
    (
        ([0], [0], [0]),
        ([1], [0], [1]),
        ([1], [2], [3]),
        ([1, 0, 1], [1, 2, 3], [2, 2, 4]),
        ([0, 0, 0], [-11, 2, 1], [-11, 2, 1]),
        ([1.1, 2.2, 3.3, 5.5, 4.4], [1, 1, 1, 1, 1], [2.1, 3.2, 4.3, 6.5, 5.4]),
    ),
)
def test_add(elements_1, elements_2, expected):
    assert (Vector(elements_1) + Vector(elements_2)) == Vector(expected)


@pytest.mark.parametrize(
    "elements_1,elements_2,expected",
    (
        ([0], [0], [0]),
        ([1], [1], [0]),
        ([1], [-1], [2]),
        ([1, 0, 1], [1, -7, 8], [0, 7, -7]),
        ([0, 0, 0], [1, 7, 9], [-1, -7, -9]),
        ([9.1, 3, 8.9], [-3, 4, 0], [12.1, -1, 8.9]),
    ),
)
def test_sub(elements_1, elements_2, expected):
    assert (Vector(elements_1) - Vector(elements_2)) == Vector(expected)


@pytest.mark.parametrize(
    "elements_1,elements_2,expected",
    (
        ([0], [0], 0),
        ([1, 2, 5], [0, 0, 0], 0),
        ([1, 1, 1], [2, 3, 4], 9),
        ([1, 0, 0], [123, 3, 1], 123),
        ([-4, 3, 2], [-1, -5, -2], -15),
        ([5, -4], [2, 1], 6),
    ),
)
def test_mul(elements_1, elements_2, expected):
    assert (Vector(elements_1) * Vector(elements_2)) == expected


@pytest.mark.parametrize(
    "elements_1,elements_2,expected",
    (
        ([1, 2, 3], [0, 0, 0], [0, 0, 0]),
        ([-3, 2, -1], [1, 0, 2], [4, 5, -2]),
        ([2, 3, -1], [3, -1, -4], [-13, 5, -11]),
        ([2, -3, -1], [3, -1, -4], [11, 5, 7]),
    ),
)
def test_vector_mul(elements_1, elements_2, expected):
    vector_1 = Vector(elements_1)
    vector_2 = Vector(elements_2)
    assert vector_1.mul_vectors(vector_2) == Vector(expected)


@pytest.mark.parametrize(
    "elements_1,elements_2", (([0], []), ([1, 1, 1], [1, 1]), ([0.1, 13.4, 5.6, 7.8], [1, 2, 3.7]))
)
def test_add_error(elements_1, elements_2):
    with pytest.raises(ArityError):
        Vector(elements_1) + Vector(elements_2)


@pytest.mark.parametrize(
    "elements_1,elements_2", (([], [0]), ([0, 1, 1, 1], [1, 1]), ([0.1, 13.4, 5.6, 7.8], [1, 2, 3.7, 5, 5]))
)
def test_sub_error(elements_1, elements_2):
    with pytest.raises(ArityError):
        Vector(elements_1) - Vector(elements_2)


@pytest.mark.parametrize(
    "elements_1,elements_2", (([], [0, 1]), ([0, 1, 1, 1], [1, 1, 0, 0, 0]), ([0.1, 13.4, 5.6, 7.8], [1, 2, 3.7, 5, 5]))
)
def test_mul_error(elements_1, elements_2):
    with pytest.raises(ArityError):
        Vector(elements_1) * Vector(elements_2)


@pytest.mark.parametrize(
    "elements_1,elements_2",
    (([], [0, 1]), ([1, 1, 1], [1, 1, 0, 0, 0]), ([0.1, 13.4, 5.6, 7], [1, 2, 3.7, 8]), ([0, 0], [0, 0])),
)
def test_mul_vectors_error(elements_1, elements_2):
    vector_1 = Vector(elements_1)
    vector_2 = Vector(elements_2)
    with pytest.raises(ArityError):
        vector_1.mul_vectors(vector_2)
