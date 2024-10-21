from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import Categorie, User, OrderItems
from db.models.model import Product


def confirm_text():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text="✅Jo'natish✅", callback_data='confirm'),
              InlineKeyboardButton(text="❌To'xtatish❌", callback_data='stop')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def confirm_inl():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='✅Tasdiqlash✅', callback_data=f'confirm_network'),
              InlineKeyboardButton(text="❌Toxtatish❌", callback_data=f'cancel_network')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


async def admins():
    ikb = InlineKeyboardBuilder()
    for i in await User.get_admins():
        ikb.add(*[
            InlineKeyboardButton(text=i.username, callback_data=f'admins_{i.id}'),
            InlineKeyboardButton(text="❌", callback_data=f'admins_delete_{i.id}')
        ])
    ikb.row(InlineKeyboardButton(text="Admin qo'shish", callback_data="admins_add"))
    ikb.row(InlineKeyboardButton(text="⬅️Ortga️", callback_data="back_settings"))
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def link(url):
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='Link', url=url))
    return ikb.as_markup()


async def inl_for_basket():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='❌ Savatni tozalash', callback_data='clear_basket'),
              InlineKeyboardButton(text='✅ Buyurtmani tasdiqlash', callback_data='confirm_orders'),
              InlineKeyboardButton(text='🔙Back🔙', callback_data=f'back_category')])
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()


async def inl_categories():
    products = await Categorie.get_all()
    ikb = InlineKeyboardBuilder()
    for i in products:
        ikb.add(*[InlineKeyboardButton(text=i.title, callback_data=f'categories_{i.id}')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


async def inl_categories_group():
    products = await Categorie.get_all()
    ikb = InlineKeyboardBuilder()
    for i in products:
        ikb.add(*[InlineKeyboardButton(text=i.title, callback_data=f'categoriesgroup_{i.id}')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


async def confirm_order_in_group(id_):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text="O'zgartirish", callback_data=f'group_change_{id_}'),
        InlineKeyboardButton(text="Qabul qilish", callback_data=f'group_confirm_{id_}')
    ])
    ikb.adjust(2)
    return ikb.as_markup()

async def change_type_office(user_id):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text="Restoran", callback_data=f"type_Restoran_{user_id}"),
        InlineKeyboardButton(text="Optom", callback_data=f'type_Optom_{user_id}')
    ])
    ikb.adjust(2)
    return ikb.as_markup()

async def change_order_in_group(order_id):
    ikb = InlineKeyboardBuilder()
    order_items: list['OrderItems'] = await OrderItems.get_order_items(int(order_id))
    for i in order_items:
        product: Product = await Product.get(i.product_id)
        ikb.add(*[
            InlineKeyboardButton(text=product.title, callback_data=f'change_group_confirms_{i.id}'),
            InlineKeyboardButton(text=str(i.count), callback_data=f'change_group_confirms_{i.id}'),
            InlineKeyboardButton(text="❌", callback_data=f'change_group_delete_{i.id}')
        ])
    ikb.row(
        InlineKeyboardButton(text="Qabul qilish", callback_data=f'change_group_confirm_{order_id}'),
        InlineKeyboardButton(text="❌Otkaz", callback_data=f'change_group_deleteorder_{order_id}'),
    )
    ikb.adjust(3, repeat=True)
    return ikb.as_markup()


# InlineKeyboardButton(text="Qo'shish", callback_data=f'change_group_add_{order_id}')

async def inl_products(category_id):
    products = await Product.get_books(category_id)
    ikb = InlineKeyboardBuilder()
    for i in products:
        ikb.add(*[InlineKeyboardButton(text=i.title, callback_data=f'product_{i.id}')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


async def inl_products_in_group(category_id):
    products = await Product.get_books(category_id)
    ikb = InlineKeyboardBuilder()
    for i in products:
        ikb.add(*[InlineKeyboardButton(text=i.title, callback_data=f'productgroup_{i.id}')])
    ikb.row(*[InlineKeyboardButton(text="Ortga", callback_data=f'productgroup_back')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def payment_true(payment, id_):
    if payment == True:
        payments = "✅To'lov qilingan"
    else:
        payments = "❌To'lov qilinmagan"
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text=payments, callback_data=f"payment_{payment}_{id_}"))
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()


def confirm_register_inl():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='✅Tasdiqlash✅', callback_data=f'confirm_register'),
              InlineKeyboardButton(text='❌Cancel❌', callback_data=f'cancel_register')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def permission_user(user_id):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='✅Ruxsat berish', callback_data=f'permission_confirm_{user_id}'),
              InlineKeyboardButton(text="❌", callback_data=f'permission_cancel_{user_id}')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()
