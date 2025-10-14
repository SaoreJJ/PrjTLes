import pytest
from src.classes import Category, Product, Smartphone, LawnGrass, CategoryIterator


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
