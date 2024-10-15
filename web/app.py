import os

import uvicorn
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy_file.storage import StorageManager
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView


from db import User, Categorie, Product, database, Order, OrderItems, Channel, About, Cart
from web.provider import UsernameAndPasswordProvider

middleware = [
    Middleware(SessionMiddleware, secret_key='1234')
]

app = Starlette(middleware=middleware)

admin = Admin(
    engine=database._engine,
    title="Aiogram Web Admin",
    base_url='/',
    auth_provider=UsernameAndPasswordProvider()
)


class ProductAdmin(ModelView):
    form_overrides = {
        'type': SQLAlchemyEnum()
    }

    form_args = {
        'type': {
            'choices': [
                ('dona', 'Dona'),
                ('kg', 'Kg')
            ]
        }
    }


class UserModelView(ModelView):
    exclude_fields_from_edit = ('created_at', 'updated_at')


class CategoryModelView(ModelView):
    exclude_fields_from_create = ('created_at', 'updated_at')
    exclude_fields_from_edit = ('created_at', 'updated_at')


class OrdersModelView(ModelView):
    exclude_fields_from_create = ('created_at', 'updated_at')
    exclude_fields_from_edit = ('created_at', 'updated_at')


admin.add_view(UserModelView(User))
admin.add_view(CategoryModelView(Categorie))
admin.add_view(ProductAdmin(Product))
admin.add_view(ModelView(About))
admin.add_view(ModelView(Order))
admin.add_view(ModelView(OrderItems))
admin.add_view(ModelView(Cart))

admin.mount_to(app)

os.makedirs("./media/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver("./media").get_container("attachment")
StorageManager.add_storage("default", container)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
