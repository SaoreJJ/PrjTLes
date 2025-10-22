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
        expected_methods = {"__init__", "__str__", "__add__", "price"}
        assert abstract_methods == expected_methods


class TestLoggingMixin:
    def test_logging_mixin_initialization(self, capsys):
        """Тестируем работу миксина логирования"""

        class TestClass(LoggingMixin):
            def __init__(self, name, value):
                self.name = name
                self.value = value
                super().__init__()

        TestClass("Test", 123)  # Создаем объект, но не сохраняем в переменную
        captured = capsys.readouterr()
        assert "TestClass('Test', 123)" in captured.out

    def test_product_with_logging(self, capsys):
        """Тестируем создание Product с логированием"""
        Product("Test Product", "Test Description", 100.0, 10)  # Создаем объект, но не сохраняем
        captured = capsys.readouterr()
        assert "Product('Test Product', 'Test Description', 100.0, 10)" in captured.out

    def test_smartphone_with_logging(self, capsys):
        """Тестируем создание Smartphone с логированием"""
        Smartphone(
            "Test Phone", "Test Description", 1000.0, 5, 95.5, "Model X", 256, "Black"
        )  # Создаем объект, но не сохраняем
        captured = capsys.readouterr()
        assert "Smartphone('Test Phone', 'Test Description', 1000.0, 5, 95.5, 'Model X', 256, 'Black')" in captured.out

    def test_lawn_grass_with_logging(self, capsys):
        """Тестируем создание LawnGrass с логированием"""
        LawnGrass(
            "Test Grass", "Test Description", 50.0, 10, "Russia", "7 days", "Green"
        )  # Создаем объект, но не сохраняем
        captured = capsys.readouterr()
        assert "LawnGrass('Test Grass', 'Test Description', 50.0, 10, 'Russia', '7 days', 'Green')" in captured.out


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


# Существующие тесты остаются без изменений...
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
        expected = 1000.0 * 2 + 1500.0 * 3  # 2000 + 4500 = 6500
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
        expected = 50.0 * 5 + 60.0 * 3  # 250 + 180 = 430
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
        assert result == 100.0 * 5 + 200.0 * 3  # 500 + 600 = 1100

    def test_base_product_addition_different_class(self):
        product = Product("Product1", "Description1", 100.0, 5)
        smartphone = Smartphone("Phone1", "Desc1", 1000.0, 2, 95.5, "Model X", 256, "Black")

        with pytest.raises(TypeError, match="Можно складывать только объекты одного класса"):
            product + smartphone


class TestProductZeroQuantity:
    def test_product_zero_quantity_raises_error(self):
        """Проверяем, что создание продукта с нулевым количеством вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Product("Invalid Product", "Description", 100.0, 0)

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


class TestZeroQuantityError:
    def test_custom_exception_raised(self, capsys):
        """Проверяем работу пользовательского исключения"""
        try:
            Product("Test Product", "Description", 100.0, 0)
        except ZeroQuantityError:
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
