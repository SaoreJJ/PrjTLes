import pytest

from src.classes import Category, Product


class TestProduct:
    def test_product_initialization(self):
        product = Product("Test Product", "Test Description", 100.0, 10)
        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 100.0
        assert product.quantity == 10


class TestCategory:
    def test_category_initialization(self):
        product = Product("Test Product", "Test Description", 100.0, 10)
        category = Category("Test Category", "Test Description", [product])
        assert category.name == "Test Category"
        assert category.description == "Test Description"
        assert len(category.products) == 1
        assert category.products[0].name == "Test Product"

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
