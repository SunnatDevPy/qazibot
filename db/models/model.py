from enum import Enum

from sqlalchemy import ForeignKey, BIGINT, Text, String, Boolean, Enum as SQLAlchemyEnum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import CreateModel, Base


class User(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(nullable=True, default=False)
    contact: Mapped[str] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    lat: Mapped[float] = mapped_column(nullable=True)
    long: Mapped[float] = mapped_column(nullable=True)
    idora: Mapped[str] = mapped_column(nullable=True)
    permission: Mapped[bool] = mapped_column(Boolean, default=False)
    idora_turi: Mapped[str] = mapped_column(String, nullable=True)
    orders: Mapped[list['Order']] = relationship('Order', back_populates='order_from_user')
    carts: Mapped[list["Cart"]] = relationship('Cart', back_populates='cart_from_user')
    confirmation_order: Mapped[list["OrderConfirmation"]] = relationship('OrderConfirmation',
                                                                         back_populates='confirmation_user')


class BooleanEnum(Enum):
    dona = "dona"
    kg = 'kg'


class Categorie(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    title: Mapped[str]
    product_ids: Mapped[list['Product']] = relationship('Product', back_populates='category')


class Product(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(Categorie.id, ondelete='CASCADE'))
    photo: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String)
    restoran_price: Mapped[int] = mapped_column(BIGINT)
    optom_price: Mapped[int] = mapped_column(BIGINT)
    type: Mapped[str] = mapped_column(String, SQLAlchemyEnum(BooleanEnum), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped['Categorie'] = relationship('Categorie', back_populates='product_ids')


class Cart(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(User.id, ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(Product.id, ondelete='CASCADE'))
    count: Mapped[float] = mapped_column(Float, nullable=True)
    cart_from_user: Mapped[list["Cart"]] = relationship('User', back_populates='carts')
    total: Mapped[int] = mapped_column(default=0)


class Order(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(User.id, ondelete='CASCADE'))
    payment: Mapped[bool] = mapped_column(Boolean, default=False)
    time: Mapped[str] = mapped_column(nullable=True)
    debt: Mapped[int] = mapped_column(nullable=True, default=0)
    debt_type: Mapped[str] = mapped_column(nullable=True)
    total: Mapped[int] = mapped_column(nullable=True)
    order_items: Mapped[list['OrderItems']] = relationship('OrderItems', back_populates='order')
    order_from_user: Mapped['User'] = relationship('User', back_populates='orders')
    delivery: Mapped[str]
    nakladnoy: Mapped[str] = mapped_column(nullable=True)


class OrderItems(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(Product.id, ondelete='CASCADE'))
    order_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(Order.id, ondelete='CASCADE'))
    count: Mapped[float] = mapped_column(Float, default=0, nullable=True)
    order: Mapped['Order'] = relationship('Order', back_populates='order_items')


class About(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    text: Mapped[int] = mapped_column(Text)


class Channel(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BIGINT)
    type: Mapped[bool]


class OrderConfirmation(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    order_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(Order.id, ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(User.id, ondelete='CASCADE'))
    confirmation_user: Mapped["User"] = relationship('User',
                                                     back_populates='confirmation_order')
