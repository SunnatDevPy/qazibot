from aiogram import html
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.text_decorations import html_decoration

from db import User, Order, Cart
from db.models.model import Product, OrderItems


def change_number(formatted_num):
    return f'{formatted_num:,}'.replace(',', ' ')


async def product_detail(product, user):
    if user.idora_turi == "Restoran":
        price = product.restoran_price
    else:
        price = product.optom_price
    text = f'''   
<b>{product.title}</b>

{product.description}
{product.type} - {change_number(price)} so'm
'''
    return text, product.photo, price


async def order_detail(order):
    order_items = await OrderItems.get_order_items(order.id)
    user: User = await User.get(order.user_id)
    time = str(order.created_at).split(".")[0]
    text = f'<b>Buyurtma soni</b>: {order.id}\n{time}\n\n'
    count = 1
    for i in order_items:
        product = await Product.get(int(i.product_id))
        if user.idora_turi == "Restoran":
            price = product.restoran_price
        else:
            price = product.optom_price
        kg = i.count if product.type == 'kg' else int(i.count)
        text += f"{count}. {product.title}: {kg} X {change_number(price)} = {change_number(int(price * kg))} so'm\n"
        count += 1
    if order.time == "O'tkazib yuborish":
        izox = ''
    elif order.time == None or len(order.time) > 5:
        izox = ''
    else:
        izox = f"<b>Izoh</b>: {order.time}"
    text += f'''
<b>Buyurtmachi</b>: {user.full_name}
<b>Idora</b>: {user.idora}
<b>Raqam</b>: {user.contact}
{izox}

<b>To'lash turi</b>: {order.debt_type}
<b>Yetkazish</b>: {order.delivery}

<b>Jami</b>: {change_number(order.total)}    
'''
    return text, user.long, user.lat


async def order_from_user(order):
    order_items = await OrderItems.get_order_items(order.id)
    user: User = await User.get(order.user_id)
    time = str(order.created_at).split(".")[0]
    text = f'Buyurtma soni: {order.id}\nBuyurtma qilingan sana: {time}\n\n'
    count = 1
    for i in order_items:
        product = await Product.get(int(i.product_id))
        if user.idora_turi == "Restoran":
            price = product.restoran_price
        else:
            price = product.optom_price
        kg = i.count if product.type == 'kg' else int(i.count)
        text += f"{count}. {product.title}: {kg} X {change_number(price)} = {change_number(int(price * kg))} so'm\n"
        count += 1
    if order.time == "O'tkazib yuborish":
        izox = ''
    elif order.time == None or len(order.time) > 5:
        izox = ''
    else:
        izox = f"<b>Izoh</b>: {order.time}"
    if order.payment == True:
        payment = "✅"
    else:
        payment = "❌"
    text += f'''
Jami: {order.total}    
Ism-familiya: {user.full_name}
Idora: {user.idora}
To'lov: {payment}
{izox}

Qarz: {change_number(order.debt)}
'''
    return text


async def detail_text_order(order_id):
    order = await Order.get(order_id)
    user: User = await User.get(order.user_id)
    time = str(order.created_at).split(".")[0]
    if order.time == "O'tkazib yuborish":
        izox = ''
    elif order.time == None or len(order.time) > 5:
        izox = ''
    else:
        izox = f"<b>Izoh</b>: {order.time}"
    text = f'''
Buyurtma soni: {order.id}  
Buyurtma qilingan sana: {time} 
    
Ism-familiya: {user.full_name}
Idora: {user.idora}
Contact: {user.contact}
{izox}
To'lov turi: {order.debt_type}
Jami: {change_number(order.total)}    
'''
    return text, user.long, user.lat


async def cart(user_id, carts):
    user = await User.get(user_id)
    count = 1
    text = html.bold('Mahsulotlar:\n\n')
    total = 0
    for i in carts:
        product: Product = await Product.get(int(i.product_id))
        if user.idora_turi == "Restoran":
            price = product.restoran_price
        else:
            price = product.optom_price
        kg = i.count if product.type == 'kg' else int(i.count)
        text += f"{html.bold(count)}. {product.title}: {kg} X {change_number(price)} = {change_number(int(price * kg))} so'm\n"
        count += 1
        total += int(price * kg)
    text += f'\nJami: {change_number(total)}'
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


async def sum_cart(user_id):
    carts = await Cart.get_cart_in_user(user_id)
    total = 0
    for i in carts:
        total += i.total
    return total


async def info_orders_from_user(user_id):
    payment_false = await Order.get_order_payment_false(int(user_id))
    payment_true = await Order.get_order_payment_true(int(user_id))
    debt = await Order.get_order_total_and_debt_from_user(int(user_id))

    return f'''
Statistika

Buyurtmalar soni: <code>{payment_false[0] + payment_true[0]}</code> ta
To'langan buyurtmalar soni: <code>{0 if payment_true[0] == None else payment_true[0]}</code> ta
To'lanmagan buyurtmalar soni: <code>{0 if payment_false[0] == None else payment_false[0]}</code> ta

To'langan: <code>{change_number(0 if payment_true[0] == None else payment_true[0])}</code>  so'm
Qoldiq: <code>{change_number(0 if payment_false[0] == None else payment_false[0])}</code> so'm
Jami: <code>{change_number(0 if debt[-1] == None else debt[-1])}</code> so'm
    '''


async def info_orders_from_admin():
    payment_false = await Order.get_order_payment_false_all()
    payment_true = await Order.get_order_payment_true_all()
    debt = await Order.get_order_total_and_debt_all()
    users = await User.count()
    return f'''
Statistika

Userlar soni: <code>{users}</code>

Buyurtmalar soni: <code>{payment_false[0] + payment_true[0]}</code> ta
To'langan buyurtmalar soni: <code>{0 if payment_true[0] == None else payment_true[0]}</code> ta
To'lanmagan buyurtmalar soni: <code>{0 if payment_false[0] == None else payment_false[0]}</code> ta

To'langan: <code>{change_number(0 if payment_true[0] == None else payment_true[0])}</code>  so'm
Qoldiq: <code>{change_number(0 if payment_false[0] == None else payment_false[0])}</code> so'm
Jami: <code>{change_number(0 if debt[-1] == None else debt[-1])}</code> so'm
    '''
