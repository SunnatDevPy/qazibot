from aiogram import Router, F, html, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from bot.buttuns.inline import change_order_in_group, get_order_me
from bot.buttuns.simple import detail_delivery, cart_detail_btn, menu_button, choose_payment, otkazish, cancel_sum
from bot.detail_text import cart, order_detail
from db import Product
from db.models.model import Order, Cart, OrderItems
from state.states import ConfirmBasket

order_router = Router()


class ChangeCartState(StatesGroup):
    permission = State()
    type = State()


@order_router.message(F.text == "◀️ Ortga")
@order_router.message(F.text.startswith("🛒Savat ("))
async def settings(message: Message):
    carts = await Cart.get_cart_in_user(message.from_user.id)
    if carts:
        text = await cart(message.from_user.id, carts)
        await message.answer("Savat menu", parse_mode="HTML", reply_markup=cart_detail_btn())
        await message.answer(text, parse_mode="HTML", reply_markup=await change_order_in_group(carts))
    else:
        await message.answer(html.bold("Savatingiz bo'sh!"), parse_mode="HTML")


@order_router.callback_query(F.data.startswith("change_cart"))
async def group_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = call.data.split('_')
    await call.answer()
    carts = await Cart.get_cart_in_user(call.from_user.id)
    if data[2] == 'delete':
        await Cart.delete(int(data[-1]))
        if len(carts) == 1:
            await call.message.delete()
            await call.message.answer(html.bold("Savatda mahsulot qolmadi!"), parse_mode="HTML",
                                      reply_markup=await menu_button(admin=False, user_id=call.from_user.id))
        else:
            await call.message.delete()
            carts = await Cart.get_cart_in_user(call.from_user.id)
            text = await cart(call.from_user.id, carts)
            await call.message.answer(text, reply_markup=await change_order_in_group(carts), parse_mode="HTML")
    elif data[2] == 'sum':
        await call.message.delete()
        await state.set_state(ChangeCartState.permission)
        await state.update_data(cart_id=data[-1])
        cart_id: Cart = await Cart.get(int(data[-1]))
        product: Product = await Product.get(cart_id.product_id)
        await call.message.answer(f"{product.title} hozirgi miqdori: {cart_id.count}\nYangi miqdorini kiriting", reply_markup=cancel_sum())


@order_router.message(ChangeCartState.permission)
async def group_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    carts: list['Cart'] = await Cart.get_cart_in_user(message.from_user.id)
    cart_id: Cart = await Cart.get(int(data.get('cart_id')))
    text = await cart(message.from_user.id, carts)
    if message.text == "❌Toxtatish❌":
        await message.answer("Protsess to'xtatildi", reply_markup=cart_detail_btn())
        await message.answer(text, reply_markup=await change_order_in_group(carts), parse_mode="HTML")
    else:
        try:
            product = await Product.get(cart_id.product_id)
            sum = float(message.text.replace(',', '.').strip())
            if '.' in message.text and product.type == "dona" or ',' in message.text and product.type == "dona":
                await message.answer(html.bold(f"Donali mahsulotga notog'ri malumot kiritdingiz!"),
                                     parse_mode="HTML")
            else:
                await Cart.update(int(data.get('cart_id')), count=sum)
                carts: list['Cart'] = await Cart.get_cart_in_user(message.from_user.id)
                text = await cart(message.from_user.id, carts)
                await message.answer("Tanlangan mahsulot o'zgardi", reply_markup=cart_detail_btn())
                await message.answer(text, reply_markup=await change_order_in_group(carts), parse_mode="HTML")
                await state.clear()
        except:
            await message.answer(f"{message.text} noto'g'ri")
            await message.answer(f"Boshqa malumot yubordingiz, yoki juda kotta son")


@order_router.message(F.text.startswith('✅ Buyurtma qilish'))
async def count_book(message: Message, state: FSMContext):
    await state.set_state(ConfirmBasket.delivery)
    await message.answer("Yetkazib berish turini tanlang", reply_markup=detail_delivery())


@order_router.message(F.text.in_(["🚕Yetkazib berish🚕", "🏃Olib ketish🏃"]), ConfirmBasket.delivery)
async def count_book(message: Message, state: FSMContext):
    await state.update_data(delivery=message.text)
    await state.set_state(ConfirmBasket.time)
    await message.answer("Izox yoki ovozli xabar qoldiring", reply_markup=otkazish())


@order_router.message(F.text.startswith('Tozalash'))
async def count_book(message: Message, state: FSMContext):
    try:
        await Cart.delete_carts(message.from_user.id)
        await message.answer("Savat tozalandi!",
                             reply_markup=await menu_button(admin=False, user_id=message.from_user.id))
    except:
        await message.answer("O'chirishda hatolik")


@order_router.message(ConfirmBasket.time)
async def count_book(message: Message, state: FSMContext):
    await state.set_state(ConfirmBasket.debt)
    if message.voice:
        await state.update_data(voice=message.voice)
    else:
        await state.update_data(time=message.text)
    await message.answer("Tanlang", reply_markup=choose_payment())


@order_router.message(ConfirmBasket.debt)
async def count_book(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(debt=message.text)
    data = await state.get_data()
    order = await Order.create(user_id=message.from_user.id, debt=0, payment=False,
                               time="O'tkazib yuborish" if data.get('voice') else data.get('text'),
                               debt_type=data.get('debt'), total=0,
                               delivery=data.get('delivery'))
    carts: list['Cart'] = await Cart.get_from_user(message.from_user.id)
    total = 0
    for i in carts:
        await OrderItems.create(product_id=i.product_id, count=i.count, order_id=order.id)
        await Cart.delete(i.id)
        total += i.total
    await Order.update(order.id, debt=total, total=total)
    text = await order_detail(order)
    await message.answer("Buyurtmangiz qabul qilindi tez orada aloqaga chiqamiz!",
                         reply_markup=await menu_button(admin=False, user_id=message.from_user.id))
    if data.get('delivery') == '🏃Olib ketish🏃':
        await message.answer_location(latitude=41.342221, longitude=69.275769)
        await message.answer("Bizning manzil, QaziSay")
    voice = data.get('voice')
    try:
        await bot.send_voice(-1002455618820, voice=voice.file_id, caption=text[0], parse_mode="HTML",
                             reply_markup=get_order_me(order.id))
    except:
        await bot.send_message(-1002455618820, text[0], parse_mode="HTML",
                               reply_markup=get_order_me(order.id))
    await state.clear()

# -1002455618820 -> Order group
# -4542185028 -> my group
