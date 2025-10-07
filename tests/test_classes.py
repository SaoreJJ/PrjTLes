import pytest

from src.classes import Category, Product


class TestProduct:
    def test_product_initialization(self):
        product = Product("Test Product", "Test Description", 100.0, 10)
        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 100.0  # Используем геттер
        assert product.quantity == 10

    def test_price_setter_positive(self):
        product = Product("Test Product", "Test Description", 100.0, 10)
        product.price = 150.0
        assert product.price == 150.0

    def test_price_setter_negative(self, capsys):
        product = Product("Test Product", "Test Description", 100.0, 10)
        product.price = -50.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0  # Цена не изменилась

    def test_price_setter_zero(self, capsys):
        product = Product("Test Product", "Test Description", 100.0, 10)
        product.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0  # Цена не изменилась

    def test_new_product_class_method(self):
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 200.0,
            "quantity": 5
        }
        product = Product.new_product(product_data)
        assert product.name == "New Product"
        assert product.description == "New Description"
        assert product.price == 200.0
        assert product.quantity == 5


class TestCategory:
    def test_category_initialization(self):
        product = Product("Test Product", "Test Description", 100.0, 10)
        category = Category("Test Category", "Test Description", [product])
        assert category.name == "Test Category"
        assert category.description == "Test Description"
        assert "Test Product, 100.0 руб. Остаток: 10 шт." in category.products

    def test_category_count(self):
        initial_count = Category.category_count
        product = Product("Test Product", "Test Description", 100.0, 10)
        category = Category("Test Category", "Test Description", [product])
        assert Category.category_count == initial_count + 1

    def test_product_count(self):
        initial_count = Category.product_count
        product1 = Product("Product1", "Description1", 100.0, 5)
        product2 = Product("Product2", "Description2", 200.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])
        assert Category.product_count == initial_count + 2

    def test_add_product(self):
        product1 = Product("Product1", "Description1", 100.0, 5)
        category = Category("Test Category", "Test Description", [product1])
        initial_product_count = Category.product_count

        product2 = Product("Product2", "Description2", 200.0, 3)
        category.add_product(product2)

        assert "Product2, 200.0 руб. Остаток: 3 шт." in category.products
        assert Category.product_count == initial_product_count + 1

    def test_products_getter_format(self):
        product = Product("Test Product", "Test Description", 100.0, 10)
        category = Category("Test Category", "Test Description", [product])
        products_str = category.products
        expected_str = "Test Product, 100.0 руб. Остаток: 10 шт.\n"
        assert products_str == expected_str

    def test_add_product_type_check(self):
        """Тест проверки типа при добавлении продукта"""
        category = Category("Test Category", "Test Description", [])

        # Должен работать с объектом Product
        product = Product("Test Product", "Test Description", 100.0, 10)
        category.add_product(product)

        # Не должен работать с другими типами
        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product("not a product")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product(123)

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product({"name": "test"})