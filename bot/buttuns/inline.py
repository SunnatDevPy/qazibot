from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import Categorie, User
from db.models.model import Product


def confirm_inl():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='✅Tasdiqlash✅', callback_data=f'confirm_network'),
              InlineKeyboardButton(text="❌Toxtatish❌", callback_data=f'cancel_network')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def get_order_me(order_id):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='✅Buyurtmani olish✅', callback_data=f'get_order_{order_id}')])
    return ikb.as_markup()


async def admins():
    ikb = InlineKeyboardBuilder()
    for i in await User.get_admins():
        ikb.add(*[
            InlineKeyboardButton(text=i.username, callback_data=f'admins_{i.id}'),
            InlineKeyboardButton(text="❌", callback_data=f'admins_delete_{i.id}')
        ])
    ikb.row(InlineKeyboardButton(text="Admin qo'shish", callback_data="admins_add"))
    ikb.row(InlineKeyboardButton(text="⬅️Ortga️", callback_data="admins_back"))
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
    ikb.row(*[InlineKeyboardButton(text="🔍Qidiruv", switch_inline_query_current_chat=' ')])
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
        InlineKeyboardButton(text="✏Taxrirlash✏", callback_data=f'group_change_{id_}'),
        InlineKeyboardButton(text="✅Tayyor✅", callback_data=f'group_confirm_{id_}')
    ])
    ikb.adjust(2)
    return ikb.as_markup()


def yolda(order_id):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text="Yo'lda", callback_data=f'delivery_start_{order_id}')])
    return ikb.as_markup()


def qayta_buyurish(order_id):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text="Qayta buyurtma berish", callback_data=f'qayta_{order_id}')])
    return ikb.as_markup()


def bordi(order_id):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text="Yetib keldi", callback_data=f'delivery_compleat_{order_id}')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


async def check_order_in_group(id_):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text="Qabul qildim", callback_data=f'check_order_{id_}')
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


async def change_order_in_group(carts):
    ikb = InlineKeyboardBuilder()
    for i in carts:
        product: Product = await Product.get(i.product_id)
        if product.type == 'dona':
            count = int(i.count)
        else:
            count = float(i.count)
        ikb.add(*[
            InlineKeyboardButton(text=product.title, callback_data=f'change_cart_confirms_{i.id}'),
            InlineKeyboardButton(text=str(count), callback_data=f'change_cart_sum_{i.id}'),
            InlineKeyboardButton(text="❌", callback_data=f'change_cart_delete_{i.id}')
        ])
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
