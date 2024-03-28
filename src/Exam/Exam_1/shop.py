from math import inf


class Product:
    def __init__(self, name: str, price: int, rating: int, count: int) -> None:
        if price < 0 or rating < 0 or count < 0:
            raise ValueError("Price, rating, count must be >= 0")
        self.name = name
        self.price = price
        self.rating = rating
        self.count = count

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Product) and (self.name, self.price, self.rating) == (
            other.name,
            other.price,
            other.rating,
        )

    def __repr__(self) -> str:
        return f"Product(name={self.name}, price={self.price}, rating={self.rating}, count={self.count})"


class Cart:
    def __init__(self) -> None:
        self.items: list[Product] = []
        self.product_names: set[str] = set()
        self.product_count = 0

    def add_product(self, new_product: Product) -> None:
        if new_product.name not in self.product_names:
            self.items.append(new_product)
            self.product_names.add(new_product.name)
            self.product_count += 1
            return
        for i in range(self.product_count):
            if self.items[i] == new_product:
                self.items[i].count += new_product.count
                return
        raise ValueError("Similar product is already in cart!")


class Shop:
    def __init__(self) -> None:
        self.items: list[Product] = list()
        self.product_names: set[str] = set()
        self.product_count = 0

    def has_product(self, current_product: Product) -> bool:
        if current_product.name not in self.product_names:
            return False
        for product in self.items:
            if product == current_product:
                if product.count >= current_product.count:
                    return True
        return False

    def add_product(self, new_product: Product) -> None:
        if new_product.name not in self.product_names:
            self.items.append(new_product)
            self.product_names.add(new_product.name)
            self.product_count += 1
            return
        for i in range(self.product_count):
            if self.items[i] == new_product:
                self.items[i].count += new_product.count
                return
        raise ValueError("Similar product is already exist!")

    def get_max_price(self) -> list[Product] | None:
        max_price = 0
        products = []
        for product in self.items:
            if product.price == max_price:
                products.append(product)
            elif product.price > max_price:
                max_price = product.price
                products = [product]
        return products

    def get_min_price(self) -> list[Product] | None:
        min_price = inf
        products = []
        for product in self.items:
            if product.price == min_price:
                products.append(product)
            elif product.price < min_price:
                min_price = product.price
                products = [product]
        return products

    def get_max_rating(self) -> list[Product] | None:
        max_rating = 0
        products = []
        for product in self.items:
            if product.rating == max_rating:
                products.append(product)
            elif product.rating > max_rating:
                max_rating = product.rating
                products = [product]
        return products

    def get_min_rating(self) -> list[Product] | None:
        min_rating = inf
        products = []
        for product in self.items:
            if product.rating == min_rating:
                products.append(product)
            elif product.rating < min_rating:
                min_rating = product.rating
                products = [product]
        return products

    def can_buy(self, cart: Cart) -> bool:
        for product in cart.items:
            if not self.has_product(product):
                return False
        return True

    def buy_cart(self, cart: Cart) -> None:
        if not self.can_buy(cart):
            raise ValueError("Shop has not some product from this cart!")
        for product in cart.items:
            if product in self.items:
                self.items[self.items.index(product)].count -= product.count


if __name__ == "__main__":
    apple = Product("apple", 12, 12, 12)
    banana = Product("banana", 50, 100, 123)
    banana_lot = Product("banana", 50, 100, 124)
    banana_fake = Product("banana", 13, 10, 1000)
    orange = Product("orange", 130, 1, 9)
    cart_1 = Cart()
    cart_2 = Cart()
    cart_3 = Cart()
    cart_1.add_product(banana)
    cart_2.add_product(banana_fake)
    cart_3.add_product(apple)
    cart_3.add_product(banana)
    shop = Shop()
    shop.add_product(apple)
    shop.add_product(banana_lot)
    shop.add_product(orange)
    print(shop.items)
    shop.buy_cart(cart_1)
    print(shop.items)
    try:
        shop.buy_cart(cart_2)
    except ValueError as e:
        print(e)
    try:
        shop.buy_cart(cart_3)
    except ValueError as e:
        print(e)
