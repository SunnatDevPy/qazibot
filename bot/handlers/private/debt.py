from aiogram import Router, F, html, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from bot.buttuns.simple import debt_check, menu_button, admin_panel
from bot.detail_text import order_from_user
from db import User, Order

debt_router = Router()


class DebtState(StatesGroup):
    search_user = State()
    button = State()
    debt = State()
    confirm = State()


@debt_router.message(F.text == 'Qarzini yopish')
async def settingss(message: Message, state: FSMContext):
    await state.set_state(DebtState.search_user)
    await message.answer("User id, Ism, Contact yoki Idora nomini kiriting", reply_markup=ReplyKeyboardRemove())


@debt_router.message(DebtState.search_user)
async def settingss(message: Message, state: FSMContext):
    await state.clear()
    try:
        user_id = await User.get(int(message.text))
    except:
        user_id = None
    username = await User.get_from_username(message.text)
    contact = await User.get_from_contact(message.text)
    idora = await User.get_from_idora(message.text)
    await state.set_state(DebtState.button)
    if username:
        user = username
    elif contact:
        user = contact
    elif idora:
        user = idora
    elif user_id:
        user = user_id
    else:
        user = None
    if user:
        orders = await Order.get_from_user(user.id)
        if orders:
            debt = 0
            for i in orders:
                if i.payment == False:
                    await message.answer(await order_from_user(i), parse_mode="HTML")
                debt += i.debt
            await state.update_data(user_ids=user.id, orders=orders, debts=debt)
            if debt == 0:
                await state.clear()
                await message.answer("Userda qarz yo'q", reply_markup=admin_panel())
            else:
                await message.answer(f"Umumiy summa: {debt}")
                await message.answer(f"Tanlang", parse_mode="HTML", reply_markup=debt_check())
        else:
            await message.answer(f"User: {user.full_name} da buyurtmalar yo'q")
    else:
        await message.answer("User topilmadi", reply_markup=admin_panel())


@debt_router.message(DebtState.button)
async def settings(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    orders = data.get('orders')
    if message.text == "Protsess to'xtatish":
        await state.clear()
        await message.answer("Admin panel", reply_markup=admin_panel())
    elif message.text == "Summa kiritish":
        await state.set_state(DebtState.debt)
        await message.answer("Summa kiriting , umumiy narxdan oshib ketmasin!", reply_markup=ReplyKeyboardRemove())
    elif message.text == "Barchasini yopish":
        for i in orders:
            if i.payment == False:
                await Order.update(i.id, debt=0, payment=True)
        else:
            await message.answer("Barcha buyurtmalar yopildi", reply_markup=admin_panel())
            await bot.send_message(data.get('user_ids'),
                                   html.bold("Barcha buyurtmalar yopildi\n🤖 Bizni tanlaganiz uchun raxmat"),
                                   parse_mode="HTML",
                                   reply_markup=await menu_button(admin=False, user_id=message.from_user.id))
            await state.clear()


@debt_router.message(DebtState.debt)
async def settings(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    total = data.get('debts')
    orders = data.get('orders')
    user_id = data.get('user_ids')
    if message.text.isdigit():
        summa = int(message.text)
        next_sum = summa
        if total >= summa:
            for i in orders:
                if next_sum == 0:
                    break
                if i.debt >= next_sum:
                    await Order.update(i.id, debt=i.debt - next_sum)
                    next_sum = 0
                else:
                    next_sum -= i.debt
                    await Order.update(i.id, debt=0, payment=True)
                    i.debt = 0
                    i.payment = True
            await message.answer(f"{total} umumiy summadan {summa} ayrildi")
            debt = 0
            for i in orders:
                if i.payment == False:
                    await message.answer(await order_from_user(i), parse_mode="HTML")
                debt += i.debt
            if debt == 0:
                await message.answer("Userda qarz yo'q", reply_markup=admin_panel())
            else:
                await message.answer(f"Umumiy summa: {debt}, Shuncha qarziz qoldi: {debt}")
                await message.answer(f"Admin panel", reply_markup=admin_panel())
                await bot.send_message(user_id,
                                       html.bold(
                                           f"Umumiy summadan: {summa} ayrildi,\nShuncha qarziz qoldi: {debt}"),
                                       parse_mode="HTML")
        else:
            await message.answer(f"{total} Umumiy summadan ko'p kiritidngiz! {summa} ", reply_markup=admin_panel())
    else:
        await message.answer("Iltimos son kiriting", reply_markup=admin_panel())
    await state.clear()
