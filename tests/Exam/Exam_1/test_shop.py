import pytest

from src.Exam.Exam_1.shop import *


def create_dummy_cart(list_product):
    cart = Cart()
    for product in list_product:
        cart.add_product(product)
    return cart


def create_dummy_shop(list_product):
    shop = Shop()
    for product in list_product:
        shop.add_product(product)
    return shop


@pytest.mark.parametrize(
    "list_product",
    (
        [
            Product("a", 1, 1, 1),
            Product(
                "b",
                2,
                2,
                2,
            ),
        ],
        [Product("a", 1, 1, 1)],
        [],
    ),
)
def test_create_shop(list_product):
    shop = create_dummy_shop(list_product)
    assert shop.items == list_product, shop.product_count == len(list_product)


@pytest.mark.parametrize(
    "list_product",
    (
        [
            Product("a", 1, 1, 1),
            Product(
                "b",
                2,
                2,
                2,
            ),
        ],
        [Product("a", 1, 1, 1)],
        [],
    ),
)
def test_create_cart(list_product):
    cart = create_dummy_cart(list_product)
    assert cart.items == list_product, cart.product_count == len(list_product)


@pytest.mark.parametrize(
    "shop_list,cart_list,expected",
    (
        (
            [
                Product("a", 1, 1, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
            [
                Product("a", 1, 1, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
            [
                Product("a", 1, 1, 0),
                Product(
                    "b",
                    2,
                    2,
                    0,
                ),
            ],
        ),
        (
            [
                Product("a", 1, 1, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
            [Product("a", 1, 1, 1)],
            [
                Product("a", 1, 1, 0),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
        ),
        ([Product("a", 1, 1, 1)], [], [Product("a", 1, 1, 1)]),
    ),
)
def test_buy_cart(shop_list, cart_list, expected):
    shop = create_dummy_shop(shop_list)
    cart = create_dummy_cart(cart_list)
    shop.buy_cart(cart)
    assert shop.items == expected


@pytest.mark.parametrize(
    "shop_list,cart_list",
    (
        (
            [
                Product("a", 1, 1, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
            [Product("c", 3, 3, 3)],
        ),
        (
            [
                Product("a", 1, 1, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
            [Product("a", 4, 4, 4)],
        ),
    ),
)
def test_error_buy_cart(shop_list, cart_list):
    shop = create_dummy_shop(shop_list)
    cart = create_dummy_cart(cart_list)
    with pytest.raises(ValueError):
        shop.buy_cart(cart)


@pytest.mark.parametrize(
    "shop_list,expected",
    (
        (
            [
                Product("a", 2, 2, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
            [
                Product("a", 2, 2, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
        ),
        (
            [
                Product("apple", 120, 1, 1),
                Product(
                    "orange",
                    20,
                    2,
                    2,
                ),
            ],
            [Product("apple", 120, 1, 1)],
        ),
        ([], []),
    ),
)
def test_max_price(shop_list, expected):
    shop = create_dummy_shop(shop_list)
    assert shop.get_max_price() == expected


@pytest.mark.parametrize(
    "shop_list,expected",
    (
        (
            [
                Product("a", 2, 2, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
            [
                Product("a", 2, 2, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
        ),
        (
            [
                Product("apple", 120, 1, 1),
                Product(
                    "orange",
                    20,
                    2,
                    2,
                ),
            ],
            [Product("orange", 20, 2, 2)],
        ),
        ([], []),
    ),
)
def test_min_price(shop_list, expected):
    shop = create_dummy_shop(shop_list)
    assert shop.get_min_price() == expected


@pytest.mark.parametrize(
    "shop_list,expected",
    (
        (
            [
                Product("a", 2, 2, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
            [
                Product("a", 2, 2, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
        ),
        (
            [
                Product("apple", 120, 20, 1),
                Product(
                    "orange",
                    20,
                    2,
                    2,
                ),
            ],
            [Product("apple", 120, 20, 1)],
        ),
        ([], []),
    ),
)
def test_max_rating(shop_list, expected):
    shop = create_dummy_shop(shop_list)
    assert shop.get_max_rating() == expected


@pytest.mark.parametrize(
    "shop_list,expected",
    (
        (
            [
                Product("a", 2, 2, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
            [
                Product("a", 2, 2, 1),
                Product(
                    "b",
                    2,
                    2,
                    2,
                ),
            ],
        ),
        (
            [
                Product("apple", 120, 20, 1),
                Product(
                    "orange",
                    20,
                    2,
                    2,
                ),
            ],
            [Product("orange", 20, 2, 2)],
        ),
        ([], []),
    ),
)
def test_max_price(shop_list, expected):
    shop = create_dummy_shop(shop_list)
    assert shop.get_min_rating() == expected


def test_add_similar_product():
    shop = create_dummy_shop([Product("apple", 100, 100, 100)])
    cart = create_dummy_cart([Product("apple", 100, 100, 100)])
    with pytest.raises(ValueError):
        shop.add_product(Product("apple", 20, 1, 1))
    with pytest.raises(ValueError):
        cart.add_product(Product("apple", 20, 1, 1))
