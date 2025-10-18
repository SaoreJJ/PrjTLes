from abc import ABC, abstractmethod


class LoggingMixin:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_name = self.__class__.__name__
        # Формируем строку с параметрами для вывода
        params = []
        if hasattr(self, 'name'):
            params.append(f"'{self.name}'")
        if hasattr(self, 'description'):
            params.append(f"'{self.description}'")
        if hasattr(self, 'price'):
            params.append(f"{self.price}")
        if hasattr(self, 'quantity'):
            params.append(f"{self.quantity}")

        # Добавляем специфичные параметры для наследников
        if hasattr(self, 'efficiency'):
            params.append(f"{self.efficiency}")
        if hasattr(self, 'model'):
            params.append(f"'{self.model}'")
        if hasattr(self, 'memory'):
            params.append(f"{self.memory}")
        if hasattr(self, 'color'):
            params.append(f"'{self.color}'")
        if hasattr(self, 'country'):
            params.append(f"'{self.country}'")
        if hasattr(self, 'germination_period'):
            params.append(f"'{self.germination_period}'")

        params_str = ", ".join(params)
        print(f"{class_name}({params_str})")


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов"""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        pass


class Product(BaseProduct, LoggingMixin):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity
        # Вызов __init__ миксина после инициализации атрибутов
        LoggingMixin.__init__(self)

    def __str__(self):
        """Строковое представление продукта"""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Сложение продуктов - возвращает сумму произведений цены на количество"""
        if type(self) != type(other):
            raise TypeError("Можно складывать только объекты одного класса")
        return self.price * self.quantity + other.price * other.quantity

    @property
    def price(self):
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с проверкой на положительное значение"""
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")

    @classmethod
    def new_product(cls, product_data: dict):
        """Класс-метод для создания нового продукта из словаря"""
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"]
        )


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        # Повторно вызываем миксин для логирования с полными параметрами
        LoggingMixin.__init__(self)

    def __add__(self, other):
        """Сложение смартфонов - только с объектами того же класса"""
        if type(self) != type(other):
            raise TypeError("Можно складывать только объекты одного класса")
        return self.price * self.quantity + other.price * other.quantity


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
        # Повторно вызываем миксин для логирования с полными параметрами
        LoggingMixin.__init__(self)

    def __add__(self, other):
        """Сложение газонной травы - только с объектами того же класса"""
        if type(self) != type(other):
            raise TypeError("Можно складывать только объекты одного класса")
        return self.price * self.quantity + other.price * other.quantity


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут списка товаров
        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        """Строковое представление категории"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self):
        """Геттер для списка товаров в формате строки"""
        products_str = ""
        for product in self.__products:
            products_str += f"{product}\n"  # Используем __str__ продукта
        return products_str

    def add_product(self, product):
        """Метод для добавления продукта в категорию с проверкой типа"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1


class CategoryIterator:
    def __init__(self, category):
        self.category = category
        self.products = category._Category__products  # Доступ к приватному атрибуту
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration