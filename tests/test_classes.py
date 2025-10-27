import pytest
from abc import ABC
from src.classes import Category, Product, Smartphone, LawnGrass, BaseProduct, LoggingMixin


class TestBaseProduct:
    def test_base_product_is_abstract(self):
        """Проверяем, что BaseProduct является абстрактным классом"""
        assert issubclass(BaseProduct, ABC)

    def test_base_product_has_abstract_methods(self):
        """Проверяем, что BaseProduct имеет абстрактные методы"""
        abstract_methods = BaseProduct.__abstractmethods__
        expected_methods = {'__init__', '__str__', '__add__', 'price'}
        assert abstract_methods == expected_methods


class TestLoggingMixin:
    def test_logging_mixin_initialization(self, capsys):
        """Тестируем работу миксина логирования"""

        class TestClass(LoggingMixin):
            def __init__(self, name, value):
                self.name = name
                self.value = value
                super().__init__()

        TestClass("Test", 123)
        captured = capsys.readouterr()
        # Проверяем только наличие класса и имени, так как value не логируется
        assert "TestClass('Test'" in captured.out

    def test_product_with_logging(self, capsys):
        """Тестируем создание Product с логированием"""
        Product("Test Product", "Test Description", 100.0, 10)
        captured = capsys.readouterr()
        assert "Product('Test Product', 'Test Description', 100.0, 10)" in captured.out

    def test_smartphone_with_logging(self, capsys):
        """Тестируем создание Smartphone с логированием"""
        Smartphone("Test Phone", "Test Description", 1000.0, 5,
                   95.5, "Model X", 256, "Black")
        captured = capsys.readouterr()
        # Проверяем части вывода, так как порядок параметров может отличаться
        assert "Smartphone('Test Phone', 'Test Description', 1000.0, 5" in captured.out
        assert "95.5" in captured.out
        assert "'Model X'" in captured.out
        assert "256" in captured.out
        assert "'Black'" in captured.out

    def test_lawn_grass_with_logging(self, capsys):
        """Тестируем создание LawnGrass с логированием"""
        LawnGrass("Test Grass", "Test Description", 50.0, 10,
                  "Russia", "7 days", "Green")
        captured = capsys.readouterr()
        # Проверяем части вывода
        assert "LawnGrass('Test Grass', 'Test Description', 50.0, 10" in captured.out
        assert "'Russia'" in captured.out
        assert "'7 days'" in captured.out
        assert "'Green'" in captured.out


class TestInheritanceChain:
    def test_product_inheritance(self):
        """Проверяем цепочку наследования Product"""
        assert issubclass(Product, BaseProduct)
        assert issubclass(Product, LoggingMixin)

    def test_smartphone_inheritance(self):
        """Проверяем цепочку наследования Smartphone"""
        assert issubclass(Smartphone, Product)
        assert issubclass(Smartphone, BaseProduct)

    def test_lawn_grass_inheritance(self):
        """Проверяем цепочку наследования LawnGrass"""
        assert issubclass(LawnGrass, Product)
        assert issubclass(LawnGrass, BaseProduct)


class TestSmartphone:
    def test_smartphone_initialization(self):
        smartphone = Smartphone("Test Phone", "Test Description", 1000.0, 5, 95.5, "Model X", 256, "Black")
        assert smartphone.name == "Test Phone"
        assert smartphone.description == "Test Description"
        assert smartphone.price == 1000.0
        assert smartphone.quantity == 5
        assert smartphone.efficiency == 95.5
        assert smartphone.model == "Model X"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_smartphone_addition_same_class(self):
        smartphone1 = Smartphone("Phone1", "Desc1", 1000.0, 2, 95.5, "Model X", 256, "Black")
        smartphone2 = Smartphone("Phone2", "Desc2", 1500.0, 3, 98.0, "Model Y", 512, "White")

        result = smartphone1 + smartphone2
        expected = 1000.0 * 2 + 1500.0 * 3
        assert result == expected

    def test_smartphone_addition_different_class(self):
        smartphone = Smartphone("Phone1", "Desc1", 1000.0, 2, 95.5, "Model X", 256, "Black")
        product = Product("Regular Product", "Desc", 500.0, 4)

        with pytest.raises(TypeError, match="Можно складывать только объекты одного класса"):
            smartphone + product


class TestLawnGrass:
    def test_lawn_grass_initialization(self):
        grass = LawnGrass("Test Grass", "Test Description", 50.0, 10, "Russia", "7 days", "Green")
        assert grass.name == "Test Grass"
        assert grass.description == "Test Description"
        assert grass.price == 50.0
        assert grass.quantity == 10
        assert grass.country == "Russia"
        assert grass.germination_period == "7 days"
        assert grass.color == "Green"

    def test_lawn_grass_addition_same_class(self):
        grass1 = LawnGrass("Grass1", "Desc1", 50.0, 5, "Russia", "7 days", "Green")
        grass2 = LawnGrass("Grass2", "Desc2", 60.0, 3, "USA", "5 days", "Dark Green")

        result = grass1 + grass2
        expected = 50.0 * 5 + 60.0 * 3
        assert result == expected

    def test_lawn_grass_addition_different_class(self):
        grass = LawnGrass("Grass1", "Desc1", 50.0, 5, "Russia", "7 days", "Green")
        smartphone = Smartphone("Phone1", "Desc1", 1000.0, 2, 95.5, "Model X", 256, "Black")

        with pytest.raises(TypeError, match="Можно складывать только объекты одного класса"):
            grass + smartphone


class TestCategoryWithNewProducts:
    def test_category_add_smartphone(self):
        category = Category("Electronics", "Electronic devices", [])
        smartphone = Smartphone("Phone1", "Desc1", 1000.0, 2, 95.5, "Model X", 256, "Black")

        category.add_product(smartphone)
        assert "Phone1, 1000.0 руб. Остаток: 2 шт." in category.products

    def test_category_add_lawn_grass(self):
        category = Category("Garden", "Garden products", [])
        grass = LawnGrass("Grass1", "Desc1", 50.0, 5, "Russia", "7 days", "Green")

        category.add_product(grass)
        assert "Grass1, 50.0 руб. Остаток: 5 шт." in category.products

    def test_category_add_invalid_type(self):
        category = Category("Test Category", "Test Description", [])

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product("not a product")


class TestProductAdditionRestrictions:
    def test_base_product_addition_same_class(self):
        product1 = Product("Product1", "Description1", 100.0, 5)
        product2 = Product("Product2", "Description2", 200.0, 3)

        result = product1 + product2
        assert result == 100.0 * 5 + 200.0 * 3

    def test_base_product_addition_different_class(self):
        product = Product("Product1", "Description1", 100.0, 5)
        smartphone = Smartphone("Phone1", "Desc1", 1000.0, 2, 95.5, "Model X", 256, "Black")

        with pytest.raises(TypeError, match="Можно складывать только объекты одного класса"):
            product + smartphone


class TestProductZeroQuantity:
    def test_product_zero_quantity_raises_value_error(self):
        """Проверяем, что создание продукта с нулевым количеством вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен") as exc_info:
            Product("Invalid Product", "Description", 100.0, 0)
        # Дополнительная проверка сообщения об ошибке
        assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)

    def test_product_positive_quantity_works(self):
        """Проверяем, что создание продукта с положительным количеством работает нормально"""
        product = Product("Valid Product", "Description", 100.0, 5)
        assert product.quantity == 5


class TestCategoryMiddlePrice:
    def test_category_middle_price_with_products(self):
        """Проверяем расчет средней цены для категории с товарами"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])

        expected_average = (100.0 + 200.0) / 2
        assert category.middle_price() == expected_average

    def test_category_middle_price_empty(self):
        """Проверяем расчет средней цены для пустой категории"""
        category = Category("Empty Category", "No products", [])
        assert category.middle_price() == 0

    def test_category_middle_price_single_product(self):
        """Проверяем расчет средней цены для категории с одним товаром"""
        product = Product("Single Product", "Desc", 150.0, 1)
        category = Category("Single Category", "One product", [product])
        assert category.middle_price() == 150.0


class TestValueErrorHandling:
    def test_value_error_handling_with_messages(self, capsys):
        """Проверяем обработку ValueError с выводом сообщений"""
        try:
            Product("Test Product", "Description", 100.0, 0)
        except ValueError:
            # Исключение должно быть перехвачено
            pass

        captured = capsys.readouterr()
        assert "Товар с нулевым количеством не может быть добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out

    def test_successful_addition_message(self, capsys):
        """Проверяем сообщение об успешном добавлении"""
        Product("Test Product", "Description", 100.0, 5)
        captured = capsys.readouterr()
        assert "Товар успешно добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out


class TestCategoryIterator:
    def test_category_iterator(self):
        """Проверяем работу итератора категории"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])

        products = list(category.get_products_list())
        assert len(products) == 2
        assert products[0].name == "Product1"
        assert products[1].name == "Product2"


class TestProductPrice:
    def test_product_price_getter(self):
        """Проверяем геттер цены продукта"""
        product = Product("Test Product", "Description", 150.0, 3)
        assert product.price == 150.0

    def test_product_price_setter_positive(self):
        """Проверяем сеттер цены продукта с положительным значением"""
        product = Product("Test Product", "Description", 150.0, 3)
        product.price = 200.0
        assert product.price == 200.0

    def test_product_price_setter_negative(self, capsys):
        """Проверяем сеттер цены продукта с отрицательным значением"""
        product = Product("Test Product", "Description", 150.0, 3)
        product.price = -100.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 150.0  # Цена не изменилась


class TestCategoryProperties:
    def test_category_string_representation(self):
        """Проверяем строковое представление категории"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])

        expected_str = "Test Category, количество продуктов: 5 шт."
        assert str(category) == expected_str

    def test_category_length(self):
        """Проверяем метод __len__ категории"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])

        assert len(category) == 2

    def test_category_products_property(self):
        """Проверяем свойство products категории"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])

        products_str = category.products
        assert "Product1, 100.0 руб. Остаток: 2 шт." in products_str
        assert "Product2, 200.0 руб. Остаток: 3 шт." in products_str


class TestProductClassMethod:
    def test_new_product_class_method(self):
        """Проверяем класс-метод new_product"""
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 250.0,
            "quantity": 4
        }
        product = Product.new_product(product_data)

        assert product.name == "New Product"
        assert product.description == "New Description"
        assert product.price == 250.0
        assert product.quantity == 4