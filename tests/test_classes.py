import pytest

from src.classes import Category, Product, CategoryIterator


class TestProduct:
    def test_product_initialization(self):
        product = Product("Test Product", "Test Description", 100.0, 10)
        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 100.0
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
        assert product.price == 100.0

    def test_price_setter_zero(self, capsys):
        product = Product("Test Product", "Test Description", 100.0, 10)
        product.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0

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

    def test_product_str_representation(self):
        product = Product("Test Product", "Test Description", 100.0, 10)
        expected_str = "Test Product, 100.0 руб. Остаток: 10 шт."
        assert str(product) == expected_str

    def test_product_addition(self):
        product1 = Product("Product1", "Description1", 100.0, 5)
        product2 = Product("Product2", "Description2", 200.0, 3)

        # 100 * 5 + 200 * 3 = 500 + 600 = 1100
        result = product1 + product2
        assert result == 1100.0

    def test_product_addition_with_different_objects(self):
        product = Product("Product1", "Description1", 100.0, 5)

        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + "invalid_object"


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
        category = Category("Test Category", "Test Description", [])

        product = Product("Test Product", "Test Description", 100.0, 10)
        category.add_product(product)

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product("not a product")

    def test_category_str_representation(self):
        product1 = Product("Product1", "Description1", 100.0, 5)
        product2 = Product("Product2", "Description2", 200.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])

        # 5 + 3 = 8
        expected_str = "Test Category, количество продуктов: 8 шт."
        assert str(category) == expected_str

    def test_category_str_with_empty_products(self):
        category = Category("Test Category", "Test Description", [])
        expected_str = "Test Category, количество продуктов: 0 шт."
        assert str(category) == expected_str


class TestCategoryIterator:
    def test_category_iterator(self):
        product1 = Product("Product1", "Description1", 100.0, 5)
        product2 = Product("Product2", "Description2", 200.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])

        products_from_iterator = []
        for product in CategoryIterator(category):
            products_from_iterator.append(product)

        assert len(products_from_iterator) == 2
        assert products_from_iterator[0].name == "Product1"
        assert products_from_iterator[1].name == "Product2"

    def test_category_iterator_empty(self):
        category = Category("Test Category", "Test Description", [])

        products_from_iterator = []
        for product in CategoryIterator(category):
            products_from_iterator.append(product)

        assert len(products_from_iterator) == 0