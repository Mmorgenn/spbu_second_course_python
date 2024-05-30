import pytest

from src.Exam.Exam_1.restaurant import *


class Tester:
    def __init__(self):
        self.rest = Restaurant("Testovoe")

    def add_dishes(self):
        for dish, dishes_type in (
            [Dish("Chiken", DishType.hot_dish, 120, 20), DishType.hot_dish],
            [Dish("Pizza", DishType.hot_dish, 250, 15), DishType.hot_dish],
            [Dish("IceCream", DishType.cold_dish, 65, 1), DishType.cold_dish],
            [Dish("ApplePie", DishType.cold_dish, 100, 25), DishType.cold_dish],
        ):
            self.rest.add_dish(dishes_type, dish)

    def add_tables(self):
        for i in range(10):
            self.rest.add_table(i)

    def add_waiter(self):
        for waiter in [Waiter("Popov", 1234), Waiter("Ivan", 5678), Waiter("Nikita", 404)]:
            self.rest.add_waiter(waiter)

    def choose_dishes(self):
        self.rest.choose_dish(Dish("IceCream", DishType.cold_dish, 65, 1), 3)
        self.rest.choose_dish(Dish("ApplePie", DishType.cold_dish, 100, 25), 3)


@pytest.mark.parametrize(
    "dish,dish_type",
    (
        (Dish("Bubu", DishType.cold_dish, 434, 123), DishType.cold_dish),
        (Dish("Gogog", DishType.hot_dish, 5678, 9), DishType.hot_dish),
        (Dish("Auau", DishType.cold_dish, 44, 12), DishType.cold_dish),
    ),
)
def test_add_dishes(dish, dish_type):
    tester = Tester()
    tester.add_dishes()
    tester.rest.add_dish(dish_type, dish)
    assert len(tester.rest.menu["hot_dish"]) + len(tester.rest.menu["cold_dish"]) == 5


@pytest.mark.parametrize("tabel_number", (11, 20, 102, 3030))
def test_add_table(tabel_number):
    tester = Tester()
    tester.add_tables()
    tester.rest.add_table(tabel_number)
    assert len(list(tester.rest.tables.keys())) == 11


@pytest.mark.parametrize("waiter", (Waiter("Vasilliy", 5278), Waiter("Amogus", 3333), Waiter("Mark", 4345)))
def test_add_waiter(waiter):
    tester = Tester()
    tester.add_waiter()
    tester.rest.add_waiter(waiter)
    assert len(tester.rest.waiters) == 4


@pytest.mark.parametrize(
    "dish,table_number",
    (
        (Dish("Chiken", DishType.hot_dish, 120, 20), 1),
        (Dish("Pizza", DishType.hot_dish, 250, 15), 7),
        (Dish("ApplePie", DishType.cold_dish, 100, 25), 5),
    ),
)
def teste_choos(dish, table_number):
    tester = Tester()
    tester.add_tables()
    tester.add_dishes()
    tester.rest.choose_dish(dish, table_number)
    assert tester.rest.tables[table_number].dishes[0] == dish


@pytest.mark.parametrize("money,expected", ((165, 0), (175, 10), (200, 35), (330, 165)))
def teste_get_change(money, expected):
    tester = Tester()
    tester.add_dishes()
    tester.add_waiter()
    tester.add_tables()
    tester.choose_dishes()
    assert tester.rest.place_order(3, money) == expected


def test_full_cycle():
    tester = Tester()
    tester.add_dishes()
    tester.add_waiter()
    tester.add_tables()
    tester.choose_dishes()
    tester.rest.place_order(3, 303)
    tester.rest.complete_order(False)
    assert tester.rest.tables[3].cooked_dishes == [Dish("IceCream", DishType.cold_dish, 65, 1)]


def test_add_dish_error():
    tester = Tester()
    tester.add_dishes()
    with pytest.raises(KeyError):
        tester.rest.add_dish(DishType.hot_dish, Dish("Chiken", DishType.hot_dish, 120, 20))


def test_add_waiter_error():
    tester = Tester()
    tester.add_waiter()
    with pytest.raises(KeyError):
        tester.rest.add_waiter(Waiter("Popov", 1234))


def test_add_table_error():
    tester = Tester()
    tester.add_tables()
    with pytest.raises(KeyError):
        tester.rest.add_table(6)
