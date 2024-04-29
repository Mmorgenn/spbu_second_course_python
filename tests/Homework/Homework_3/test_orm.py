from dataclasses import dataclass
from json import loads

import pytest

from src.Homework.Homework_3.orm import ORM, JsonError


@dataclass
class Product(ORM):
    name: str | None = None
    price: int | None = None
    rating: int | None = None
    count: int | None = None


@dataclass
class Weather(ORM):
    temp: float | None = None
    wind_speed: float | None = None
    humidity: int | None = None


class Foo(ORM):
    pass


@pytest.mark.parametrize(
    "orm,data,keys,expected",
    (
        (
            Product(),
            {"name": "apple", "price": 10, "rating": 5, "count": 100},
            ("name", "price", "rating", "count"),
            ["apple", 10, 5, 100],
        ),
        (
            Product(),
            {"name": "banana", "price": 25, "rating": 4, "count": 123, "type": "fruit"},
            ("name", "price", "rating", "count"),
            ["banana", 25, 4, 123],
        ),
        (Weather(), {"temp": 12.5, "humidity": 66}, ("temp", "humidity"), [12.5, 66]),
    ),
)
def test_get_item(orm, data, keys, expected):
    current_orm = orm.upload_dict(data)
    assert [getattr(current_orm, i) for i in keys] == expected


@pytest.mark.parametrize(
    "orm,data,expected",
    (
        (Product(), {"name": "apple", "price": 10, "rating": 5, "count": 100}, {"name": "apple", "price": 10, "rating": 5, "count": 100}),
        (Product(), {"name": "banana", "price": 25, "rating": 4, "count": 123, "type": "fruit"}, {"name": "banana", "price": 25, "rating": 4, "count": 123}),
        (Weather(), {"temp": 12.5, "wind_speed": 10.5, "humidity": 66}, {"temp": 12.5, "wind_speed": 10.5, "humidity": 66}),
    ),
)
def test_dump(orm, data, expected):
    current_orm = orm.upload_dict(data)
    result = current_orm.dump()
    assert loads(result) == expected


@pytest.mark.parametrize(
    "orm,data,key,value,expected",
    (
        (Product(), {"name": "apple", "price": 10, "rating": 5, "count": 100}, "rating", 1, {"name": "apple", "price": 10, "rating": 1, "count": 100}),
        (Product(), {"name": "banana", "price": 25, "rating": 4, "count": 123, "type": "fruit"}, "count", 90, {"name": "banana", "price": 25, "rating": 4, "count": 90}),
        (Weather(), {"temp": 12.5, "wind_speed": 10.5, "humidity": 66}, "temp", 0.0, {"temp": 0.0, "wind_speed": 10.5, "humidity": 66}),
    ),
)
def test_dump_changed(orm, data, key, value, expected):
    current_orm = orm.upload_dict(data)
    setattr(current_orm, key, value)
    result = current_orm.dump()
    assert loads(result) == expected


@pytest.mark.parametrize(
    "orm,data,key",
    (
        (Product(), dict(), "name"),
        (Product(), {"name": "orange", "count": 1, "type": "fruit"}, "rating"),
        (Weather(), {"temp": 12.5, "humidity": 66}, "wind_speed"),
    ),
)
def test_get_item_error(orm, data, key):
    current_orm = orm.upload_dict(data)
    with pytest.raises(JsonError):
        getattr(current_orm, key)


def test_dump_error():
    with pytest.raises(TypeError):
        Foo().dump()
