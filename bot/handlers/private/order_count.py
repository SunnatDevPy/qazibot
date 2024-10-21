from aiogram import Router, F, html, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.buttuns.inline import confirm_order_in_group
from bot.buttuns.simple import detail_delivery, cart_detail_btn, menu_button, choose_payment
from bot.detail_text import cart, order_detail
from db.models.model import Order, Cart, OrderItems
from state.states import ConfirmBasket

order_router = Router()


@order_router.message(F.text.startswith("🛒Savat"))
async def settings(message: Message):
    carts = await Cart.get_cart_in_user(message.from_user.id)
    if carts:
        text = await cart(message.from_user.id, carts)
        await message.answer(text, parse_mode="HTML", reply_markup=cart_detail_btn())
    else:
        await message.answer(html.bold("Savatingiz bo'sh!"), parse_mode="HTML")


@order_router.message(F.text.startswith('✅ Buyurtma qilish'))
async def count_book(message: Message, state: FSMContext):
    await state.set_state(ConfirmBasket.delivery)
    await message.answer("Yetkazib berish turini tanlang", reply_markup=detail_delivery())


@order_router.message(F.text.in_(["🚕Yetkazib berish🚕", "🏃Olib ketish🏃"]), ConfirmBasket.delivery)
async def count_book(message: Message, state: FSMContext):
    await state.update_data(delivery=message.text)
    await state.set_state(ConfirmBasket.time)
    await message.answer("Sana va vaqtni kiriting", reply_markup=ReplyKeyboardRemove())
    await message.answer("Masalan 12.02.2024 16:00", reply_markup=None)


@order_router.message(F.text.startswith('Tozalash'))
async def count_book(message: Message, state: FSMContext):
    try:
        await Cart.delete_carts(message.from_user.id)
        await message.answer("Savat tozalandi!", reply_markup=menu_button(admin=False))
    except:
        await message.answer("O'chirishda hatolik")


@order_router.message(ConfirmBasket.time)
async def count_book(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(ConfirmBasket.debt)
    await message.answer("Tanlang", reply_markup=choose_payment())


@order_router.message(ConfirmBasket.debt)
async def count_book(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(debt=message.text)
    data = await state.get_data()
    order = await Order.create(user_id=message.from_user.id, debt=0, payment=False,
                               time=data.get('time'), debt_type=data.get('debt'), total=0,
                               delivery=data.get('delivery'))
    carts: list['Cart'] = await Cart.get_from_user(message.from_user.id)
    total = 0
    for i in carts:
        await OrderItems.create(product_id=i.product_id, count=i.count, order_id=order.id)
        await Cart.delete(i.id)
        total += i.total
    await Order.update(order.id, debt=total, total=total)
    text = await order_detail(order)
    await message.answer("Buyurtmangi qabul qilindi tez orada aloqaga chiqamiz!",
                         reply_markup=menu_button(admin=False))
    if data.get('delivery') == '🏃Olib ketish🏃':
        await message.answer_location(latitude=41.342221, longitude=69.275769)
        await message.answer("Bizning manzil, QaziSay")
    await bot.send_message(-1002455618820, text[0], reply_markup=await confirm_order_in_group(order.id))
    await state.clear()

# -1002455618820 -> Order group
# -4542185028 -> my group