from enum import Enum
from queue import Queue


class DishType(Enum):
    hot_dish: str = "hot_dish"
    cold_dish: str = "cold_dish"


class Dish:
    def __init__(self, name: str, dish_type: DishType, price: int, preparation_time: int) -> None:
        self.name: str = name
        self.dish_type: DishType = dish_type
        self.price: int = price
        self.preparation_time: int = preparation_time

    def __repr__(self) -> str:
        return f"{self.name}: (Price: {self.price}, Prep Time: {self.preparation_time} mins)"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Dish) and (self.name, self.price, self.dish_type, self.preparation_time) == (
            other.name,
            other.price,
            other.dish_type,
            other.preparation_time,
        )


class Table:
    def __init__(self) -> None:
        self.dishes: list[Dish] = []
        self.cooked_dishes: list[Dish] = []

    def get_table_amount(self) -> int:
        table_amount = 0
        for dish in self.dishes:
            table_amount += dish.price
        return table_amount

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Table) and self.dishes == other.dishes


class Kitchen:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hot_order: Queue[tuple[int, Dish]] = Queue()
        self.cold_order: Queue[tuple[int, Dish]] = Queue()

    def add_order(self, table_number: int, order: list[Dish]) -> None:
        for dish in order:
            if dish.dish_type == DishType.hot_dish:
                self.hot_order.put((table_number, dish))
            elif dish.dish_type == DishType.cold_dish:
                self.cold_order.put((table_number, dish))
            else:
                raise KeyError("Wrong dish type")

    def cook_dish(self, hot_order: bool = True) -> tuple[int, Dish]:
        queue = self.hot_order if hot_order else self.cold_order
        if queue.empty():
            raise KeyError("There are no suitable orders")
        result = queue.get()
        # Представьте что здесь какая-то готовка
        return result


class Waiter:
    def __init__(self, name: str, personal_id: int) -> None:
        self.name: str = name
        self.personal_id: int = personal_id

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Waiter) and (self.name == other.name,) and (self.personal_id == other.personal_id)

    def take_order(self, money: int, table_number: int, table: Table, kitchen: Kitchen) -> int:
        table_amount = table.get_table_amount()
        if table_amount > money:
            raise ValueError("Insufficient funds!")
        kitchen.add_order(table_number, table.dishes)
        change = money - table_amount
        return change

    def complete_order(self, cooked_dishes: tuple[Dish], table: Table) -> None:
        table.cooked_dishes += cooked_dishes


class Restaurant:
    def __init__(self, name: str):
        self.name: str = name
        self.menu: dict[str, list[Dish]] = {"hot_dish": [], "cold_dish": []}
        self.waiters: list[Waiter] = []
        self.waiters_queue: Queue[Waiter] = Queue()
        self.tables: dict[int, Table] = {}
        self.kitchen = Kitchen(f"Kitchen of {self.name}")

    def add_dish(self, type_dish: DishType, dish: Dish) -> None:
        if dish in self.menu[type_dish.value]:
            raise KeyError("Such dishis already exist")
        self.menu[type_dish.value].append(dish)

    def add_waiter(self, waiter: Waiter) -> None:
        if waiter in self.waiters:
            raise KeyError("Such waiter is alredy exist. Try change personal code")
        self.waiters.append(waiter)
        self.waiters_queue.put(waiter)

    def add_table(self, table_number: int) -> None:
        if table_number in self.tables.keys():
            raise KeyError("Such table is already exist")
        self.tables[table_number] = Table()

    def get_menu_list(self, type_dish: str) -> str:
        return "\n".join([f"{i}" for i in self.menu[type_dish]])

    def get_menu(self) -> str:
        return "\n".join([self.get_menu_list(type_dish) for type_dish in self.menu.keys()])

    def choose_dish(self, dish: Dish, table_number: int) -> None:
        current_table = self.tables.get(table_number, None)
        if current_table is None:
            raise KeyError("Such table is not found")
        if not any([dish in self.menu[key] for key in self.menu.keys()]):
            raise ValueError("Such dish is not found")
        current_table.dishes.append(dish)

    def place_order(self, table_number: int, money: int) -> int:
        if table_number not in self.tables.keys():
            raise KeyError("Such table is not found")
        if self.waiters_queue.empty():
            raise KeyError("There are no available waiters")
        waiter = self.waiters_queue.get()
        table = self.tables[table_number]
        change = waiter.take_order(money, table_number, table, self.kitchen)
        self.waiters_queue.put(waiter)
        return change

    def cook_dish(self, hot_dish: bool = True) -> tuple[int, tuple[Dish]] | None:
        try:
            result = self.kitchen.cook_dish(hot_dish)
        except KeyError:
            return None
        return result[0], result[1:]

    def complete_order(self, hot_dish: bool = True) -> None:
        if self.waiters_queue.empty():
            raise KeyError("There are no available waiters")
        result = self.cook_dish(hot_dish)
        if result is None:
            return
        table_number, dishes = result
        table = self.tables[table_number]
        waiter = self.waiters_queue.get()
        waiter.complete_order(dishes, table)
        self.waiters_queue.put(waiter)
