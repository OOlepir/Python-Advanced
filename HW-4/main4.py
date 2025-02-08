from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Numeric, Boolean, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime, timedelta

Base = declarative_base()

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Numeric)
    created_at = Column(DateTime)
    user = relationship("User", back_populates="orders")


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")


Base.metadata.create_all(engine)

# Задание 1. Наполнение данными. Добавьте в базу данных категории и продукты.
categories = [
    Category(name="Электроника", description="Гаджеты и устройства."),
    Category(name="Книги", description="Печатные книги и электронные книги."),
    Category(name="Одежда", description="Одежда для мужчин и женщин.")
]
session.add_all(categories)
session.commit()

products = [
    Product(name="Смартфон", price=299.99, in_stock=True, category=categories[0]),
    Product(name="Ноутбук", price=499.99, in_stock=True, category=categories[0]),
    Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=categories[1]),
    Product(name="Джинсы", price=40.50, in_stock=True, category=categories[2]),
    Product(name="Футболка", price=20.00, in_stock=True, category=categories[2])
]
session.add_all(products)
session.commit()

user1 = User(name="Alice", age=30)
user2 = User(name="Bob", age=22)
session.add_all([user1, user2])
session.commit()

order1 = Order(user_id=user1.id, amount=100.50, created_at=datetime.now() - timedelta(days=1))
order2 = Order(user_id=user1.id, amount=200.75, created_at=datetime.now())
order3 = Order(user_id=user2.id, amount=80.99, created_at=datetime.now() - timedelta(days=2))
session.add_all([order1, order2, order3])
session.commit()




# Задание 2. Чтение данных
# Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с
# ней продукты, включая их названия и цены.
all_categories = session.query(Category).all()
for category in all_categories:
    print(f"Категория: {category.name}")
    for product in category.products:
        print(f"  Продукт: {product.name}, Цена: {product.price}")



# Задание 3. Обновление данных
# Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на
# 349.99.
product_to_update = session.query(Product).filter(Product.name == "Смартфон").first()
if product_to_update:
    product_to_update.price = 349.99
    session.commit()

# Задание 4. Агрегация и группировка
# Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой
# категории.

product_counts = session.query(Category.name, func.count(Product.id)).join(Product).group_by(Category.name).all()
for category_name, count in product_counts:
    print(f"Категория: {category_name}, Количество продуктов: {count}")

# Задание 5. Группировка с фильтрацией
# Отфильтруйте и выведите только те категории, в которых более одного продукта.

filtered_categories = (
    session.query(Category.name, func.count(Product.id))
    .join(Product)
    .group_by(Category.name)
    .having(func.count(Product.id) > 1)
    .all()
)


for category_name, count in filtered_categories:
    print(f"Категория: {category_name}, Количество продуктов: {count}")
