from sqlalchemy import delete as sqlalchemy_delete, DateTime, update as sqlalchemy_update, select, func, desc
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker, Mapped, mapped_column

from config import conf


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(
            conf.db.db_url,
        )
        self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # async def drop_all(self):
    #     async with self._session.begin() as conn:
    #         await conn.run_sync(Base.metadata.drop_all)


db = AsyncDatabaseSession()
db.init()


class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def get_admins(cls):
        query = select(cls).where(cls.is_admin == True)
        return (await db.execute(query)).scalars()

    @classmethod
    async def get_from_user(cls, user_id):
        query = select(cls).where(cls.user_id == user_id).order_by(cls.id)
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_cart_in_user(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_order_items(cls, order_id):
        query = select(cls).where(cls.order_id == order_id)
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_orders_count(cls, user_id):
        query = select(func.count(cls.id)).where(cls.user_id == user_id)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_product_in_cart(cls, user_id, product_id):
        query = select(cls).where(cls.user_id == user_id, cls.product_id == product_id)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_confirm_order(cls, user_id, order_id):
        query = select(cls).where(cls.user_id == user_id, cls.order_id == order_id)
        return (await db.execute(query)).scalar()

    @classmethod
    async def create(cls, **kwargs):  # Create
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def update_channel(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.chat_id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get(cls, id_):
        query = select(cls).where(cls.id == id_)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_from_username(cls, username):
        query = select(cls).filter(cls.username.ilike(username + '%'))
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_from_contact(cls, contact):
        query = select(cls).filter(cls.contact.ilike(contact + '%'))
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_from_idora(cls, idora):
        query = select(cls).filter(cls.idora.ilike(idora + '%'))
        return (await db.execute(query)).scalar()

    @classmethod
    async def count(cls):
        query = select(func.count(cls.id))
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_true(cls):
        query = select(cls).where(cls.type == True)
        return (await db.execute(query)).scalar()

    @classmethod
    async def delete_orders(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.user_id == id_)
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def delete_carts(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.user_id == id_)
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get_books(cls, id_):
        query = select(cls).where(cls.category_id == id_).order_by(cls.id)
        return (await db.execute(query)).scalars()

    @classmethod
    async def get_history(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        return (await db.execute(query)).scalars()

    @classmethod
    async def get_order_payment_true(cls, user_id):
        query = select(func.count(cls.id), func.sum(cls.total)).where(cls.user_id == user_id, cls.payment == True)
        result = (await db.execute(query)).one()
        count, total_sum = result
        return count, total_sum

    @classmethod
    async def get_order_payment_true_all(cls):
        query = select(func.count(cls.id), func.sum(cls.total)).where(cls.payment == True)
        result = (await db.execute(query)).one()
        count, total_sum = result
        return count, total_sum

    @classmethod
    async def get_order_payment_false(cls, user_id):
        query = select(func.count(cls.id), func.sum(cls.debt)).where(cls.user_id == user_id, cls.payment == False)
        result = (await db.execute(query)).one()
        count, total_sum = result
        return count, total_sum

    @classmethod
    async def get_order_payment_false_all(cls):
        query = select(func.count(cls.id), func.sum(cls.debt)).where(cls.payment == False)
        result = (await db.execute(query)).one()
        count, total_sum = result
        return count, total_sum

    @classmethod
    async def get_order_total_and_debt_from_user(cls, user_id):
        query = select(func.sum(cls.debt), func.sum(cls.total)).where(cls.user_id == user_id)
        result = (await db.execute(query)).one()
        count, total_sum = result
        return count, total_sum

    @classmethod
    async def get_order_total_and_debt_all(cls):
        query = select(func.sum(cls.debt), func.sum(cls.total))
        result = (await db.execute(query)).one()
        count, total_sum = result
        return count, total_sum

    @classmethod
    async def get_all(cls):
        return (await db.execute(select(cls).order_by(cls.id))).scalars().all()


class Base(AsyncAttrs, DeclarativeBase, AbstractClass):
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower() + "s"


class CreateModel(Base, AbstractClass):
    __abstract__ = True
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
