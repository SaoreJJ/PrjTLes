from src.classes import Product, Category

if __name__ == '__main__':
    # Тестирование исключения при нулевом количестве
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(f"Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством: {e}")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    # Создание обычных продуктов
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(f"Средняя цена в категории '{category1.name}': {category1.middle_price()} руб.")

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(f"Средняя цена в пустой категории: {category_empty.middle_price()} руб.")