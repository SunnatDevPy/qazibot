from aiogram import html
from aiogram.utils.text_decorations import html_decoration

from db import User, Order
from db.models.model import Product, Cart, OrderItems


async def product_detail(product):
    text = html_decoration.bold(f'''   
Nomi: {product.title}
Narxi: {product.price} so'm
Turi: {product.type}
Qo'shimcha: {product.description}
''')
    return text, product.photo


async def order_detail(order):
    order_items = await OrderItems.get_order_items(order.id)
    user: User = await User.get(order.user_id)
    text = f'Buyurtma soni: {order.id}\n\n'
    count = 1
    total = 0
    for i in order_items:
        product = await Product.get(int(i.product_id))
        kg = i.count if product.type == 'kg' else int(i.count)
        text += f"{count}. {product.title}: {kg} X {product.price} = {int(product.price * kg)} so'm\n"
        count += 1
        total += int(product.price * kg)
    text += f'''
Ism-familiya: {user.full_name}
Idora: {user.idora}
Raqam: {user.contact}
To'lash turi: {order.debt_type}
Yetkazish: {order.delivery}
Vaqt: {order.time}
Jami: {total}    
'''
    return text, user.long, user.lat


async def order_from_user(order):
    order_items = await OrderItems.get_order_items(order.id)
    user: User = await User.get(order.user_id)
    text = f'Buyurtma soni: {order.id}\n\n'
    count = 1
    for i in order_items:
        product = await Product.get(int(i.product_id))
        kg = i.count if product.type == 'kg' else int(i.count)
        text += f"{count}. {product.title}: {kg} X {product.price} = {int(product.price * kg)} so'm\n"
        count += 1
    if order.payment == True:
        payment = "to'landi"
    else:
        payment = "to'lanmadi"
        text += f'''
Ism-familiya: {user.full_name}
Idora: {user.idora}
To'lov: {payment}
Qarz: {order.debt}

Jami: {order.total}    
'''
    return text


async def detail_text_order(order_id):
    order = await Order.get(order_id)
    user: User = await User.get(order.user_id)
    text = f'''
Buyurtma soni: {order.id}   
    
Ism-familiya: {user.full_name}
Idora: {user.idora}
Contact: {user.contact}
Vaqti: {order.time}
To'lov turi: {order.debt_type}
Jami: {order.total}    
'''
    return text, user.long, user.lat


async def cart(user_id):
    carts: list['Cart'] = await Cart.get_cart_in_user(user_id)
    count = 1
    text = html.bold('Mahsulotlar:\n\n')
    for i in carts:
        product: Product = await Product.get(int(i.product_id))
        kg = i.count if product.type == 'kg' else int(i.count)
        text += f"{html.bold(count)}. {product.title}: {kg} X {product.price} = {int(product.price * kg)} so'm\n"
        count += 1
    return text


# import bcrypt
#
# key = bcrypt.hashpw(b'Mirzolim99', bcrypt.gensalt(12))
# print(key)


def register_detail(msg, data=None):
    return html_decoration.bold(f'''
Ism-familiya: {data.get('full_name')}
Idora: {data.get("idora")}
Username: @{msg.from_user.username}
☎Raqam: {data.get('contact')}
''')
