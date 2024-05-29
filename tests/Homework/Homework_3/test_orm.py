from dataclasses import dataclass
from json import loads
from typing import List

import pytest

from src.Homework.Homework_3.orm import JsonError, ORMMeta, dump_dataclass


@dataclass
class Product(metaclass=ORMMeta):
    name: str
    price: int
    rating: int
    count: int


@dataclass
class Weather(metaclass=ORMMeta):
    temp: float
    wind_speed: float
    humidity: int


@dataclass
class Person(metaclass=ORMMeta):
    name: str
    surname: str
    age: int


@dataclass
class Worker(metaclass=ORMMeta):
    info: Person
    profession: str


@dataclass
class Job(metaclass=ORMMeta):
    workers: List[Worker]


@pytest.mark.parametrize(
    "orm,data,keys,expected",
    (
        (
            Product,
            {"name": "apple", "price": 10, "rating": 5, "count": 100},
            ("name", "price", "rating", "count"),
            ["apple", 10, 5, 100],
        ),
        (
            Product,
            {"name": "banana", "price": 25, "rating": 4, "count": 123, "type": "fruit"},
            ("name", "price", "rating", "count"),
            ["banana", 25, 4, 123],
        ),
        (Weather, {"temp": 12.5, "humidity": 66}, ("temp", "humidity"), [12.5, 66]),
    ),
)
def test_get_item(orm, data, keys, expected):
    current_orm = orm.parse_json(data)
    assert [getattr(current_orm, i) for i in keys] == expected


@pytest.mark.parametrize(
    "data,key,expected",
    (
        ({"profession": "economist", "info": {"name": "Albert"}}, "name", "Albert"),
        ({"profession": "economist", "info": {"name": "Bob", "surname": "White", "age": 25}}, "age", 25),
        (
            {"profession": "economist", "info": {"name": "Chu", "surname": "Ling", "age": 27, "nick": "Greedy"}},
            "surname",
            "Ling",
        ),
    ),
)
def test_get_item_branching(data, key, expected):
    current_orm = Worker.parse_json(data)
    assert getattr(current_orm.info, key) == expected


@pytest.mark.parametrize(
    "orm,data,expected",
    (
        (
            Product,
            {"name": "apple", "price": 10, "rating": 5, "count": 100},
            {"name": "apple", "price": 10, "rating": 5, "count": 100},
        ),
        (
            Product,
            {"name": "banana", "price": 25, "rating": 4, "count": 123, "type": "fruit"},
            {"name": "banana", "price": 25, "rating": 4, "count": 123},
        ),
        (
            Weather,
            {"temp": 12.5, "wind_speed": 10.5, "humidity": 66},
            {"temp": 12.5, "wind_speed": 10.5, "humidity": 66},
        ),
        (
            Worker,
            {"profession": "economist", "info": {"name": "Bob", "surname": "White", "age": 25}},
            {"profession": "economist", "info": {"name": "Bob", "surname": "White", "age": 25}},
        ),
    ),
)
def test_dump(orm, data, expected):
    current_orm = orm.parse_json(data)
    result = dump_dataclass(current_orm)
    assert loads(result) == expected


@pytest.mark.parametrize(
    "orm,data,key,value,expected",
    (
        (
            Product,
            {"name": "apple", "price": 10, "rating": 5, "count": 100},
            "rating",
            1,
            {"name": "apple", "price": 10, "rating": 1, "count": 100},
        ),
        (
            Product,
            {"name": "banana", "price": 25, "rating": 4, "count": 123, "type": "fruit"},
            "count",
            90,
            {"name": "banana", "price": 25, "rating": 4, "count": 90},
        ),
        (
            Weather,
            {"temp": 12.5, "wind_speed": 10.5, "humidity": 66},
            "temp",
            0.0,
            {"temp": 0.0, "wind_speed": 10.5, "humidity": 66},
        ),
    ),
)
def test_dump_changed(orm, data, key, value, expected):
    current_orm = orm.parse_json(data)
    setattr(current_orm, key, value)
    result = dump_dataclass(current_orm)
    assert loads(result) == expected


@pytest.mark.parametrize(
    "orm,data,key",
    (
        (Product, dict(), "name"),
        (Product, {"name": "orange", "count": 1, "type": "fruit"}, "rating"),
        (Weather, {"temp": 12.5, "humidity": 66}, "wind_speed"),
    ),
)
def test_get_item_error(orm, data, key):
    current_orm = orm.parse_json(data)
    with pytest.raises(JsonError):
        getattr(current_orm, key)


def test_json_in_json():
    orm = Worker.parse_json({"info": {"name": "Bob", "surname": "Bobov", "age": 27}, "profession": "CoolDude"})
    assert isinstance(orm.info, Person)


def test_list_jsons():
    orm = Job.parse_json(
        {
            "workers": [
                {"info": {"name": "Bob", "surname": "Bobov", "age": 27}, "profession": "CoolDude"},
                {"info": {"name": "Ivan", "surname": "Ivanov", "age": 18}, "profession": "Barber"},
                {"info": {"name": "Den", "surname": "Ben", "age": 33}, "profession": "Butcher"},
            ]
        }
    )
    assert len(orm.workers) == 3 and all([isinstance(i, Worker) for i in orm.workers])
