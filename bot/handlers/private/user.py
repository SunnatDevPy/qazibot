from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from bot.buttuns.inline import admins, payment_true
from bot.buttuns.simple import get_contact, get_location, change_user_btn, admin_panel
from bot.detail_text import register_detail, order_from_user
from db import User
from db.models.model import About, Order
from state.states import ChangeUserState, GetOrder

user_router = Router()


@user_router.message(F.text.startswith('👤Mening ma\'lumotlarim👤'))
async def count_book(message: Message):
    user = await User.get(message.from_user.id)
    await message.answer(
        register_detail(message, {"full_name": user.full_name, "contact": user.contact, "idora": user.idora}),
        parse_mode='HTML', reply_markup=change_user_btn())
    await message.answer_location(longitude=user.long, latitude=user.lat)


@user_router.message(F.text.in_(["Ism", "Contact", "Locatsiya", "Idora"]))
async def count_book(message: Message, state: FSMContext):
    await state.set_state(ChangeUserState.type)
    text = message.text
    if text == "Ism":
        await message.answer("Ismingizni kiriting", reply_markup=ReplyKeyboardRemove())
    elif text == "Contact":
        await message.answer("Contactingizni kiriting", reply_markup=get_contact())
    elif text == "Locatsiya":
        await state.update_data(text=text)
        await message.answer("Locatsiyangizni kiriting", reply_markup=get_location())


@user_router.message(ChangeUserState.type)
async def count_book(message: Message, state: FSMContext):
    data = await state.get_data()
    user = await User.get(message.from_user.id)
    if message.contact and data.get('text') == "Contact":
        await User.update(message.from_user.id, contact=str(message.contact.phone_number))
        await message.answer("Contactingiz o'zgardi")
    elif message.location and data.get('text') == "Loacatsiya":
        await User.update(message.from_user.id, long=message.location.longitude, lat=message.location.latitude)
        await message.answer("Locatsiyangiz o'zgardi")
    elif message.text and data.get('text') == "Ism":
        await User.update(message.from_user.id, full_name=message.text)
        await message.answer("Ismingiz o'zgardi")
    await message.answer(
        register_detail(message, {"full_name": user.full_name, "contact": user.contact, "idora": user.idora}),
        parse_mode='HTML', reply_markup=change_user_btn())
    await state.clear()


@user_router.message(F.text == '📃Buyurtmalarim📃')
async def count_book(message: Message):
    owner = await Order.get_from_user(message.from_user.id)
    if owner:
        for i in owner:
            await message.answer(await order_from_user(i), parse_mode="HTML")
    else:
        await message.answer("Siz hali buyurtma qilmadingiz")


@user_router.message(F.text == '📝Qoldiq')
async def count_book(message: Message):
    owner = await Order.get_from_user(message.from_user.id)
    if owner:
        qarz = 0
        for i in owner:
            if i.payment == False:
                qarz += i.debt
        else:
            await message.answer(f"Sizning qarzingiz: {qarz} so'm")
    else:
        await message.answer("Hozircha sizda qarz yo'q")


@user_router.message(F.text == "Do'kon haqida")
async def count_book(message: Message, state: FSMContext):
    about = await About.get_all()
    if about:
        await message.answer(about[0].text, parse_mode="HTML")
    else:
        await message.answer("Malumot yo'q")


#
@user_router.message(F.text == 'Settings')
async def count_book(message: Message):
    if message.from_user.id in [5649321700, 279361769] + [i for i in await User.get_admins()]:
        await message.answer("Admin panel", reply_markup=admin_panel())
    else:
        await message.answer(f"Sizda huquq yo'q")


@user_router.message(F.text == 'Userlar soni')
async def count_book(message: Message, state: FSMContext):
    count = await User.count()
    await message.answer(f"Userlar soni: {count}", reply_markup=admin_panel())


@user_router.message(F.text == "Admin qo'shish")
async def count_book(message: Message):
    if message.from_user.id in [5649321700, 279361769] + [i for i in await User.get_admins()]:
        await message.answer(html.bold("Adminlar ro'yxati"), parse_mode='HTML', reply_markup=await admins())
    else:
        await message.answer(f"Sizda huquq yo'q")


@user_router.message(F.text == "To'lanmagan buyurtmalar")
async def count_book(message: Message):
    if message.from_user.id in [5649321700, 279361769] + [i for i in await User.get_admins()]:
        owner = await Order.get_all()
        if owner:
            for i in owner:
                if i.payment == False:
                    await message.answer(await order_from_user(i), parse_mode="HTML",
                                         reply_markup=payment_true(i.payment, i.id))
        else:
            await message.answer(f"Bunday buyurtma yo'q")
    else:
        await message.answer(f"Sizda huquq yo'q")


@user_router.message(F.text == "Id bo'yicha buyurtma")
async def count_book(message: Message, state: FSMContext):
    await state.set_state(GetOrder.id)
    await message.answer(f"Buyurtmani id sini kiriting")


@user_router.message(GetOrder.id)
async def count_book(message: Message, state: FSMContext):
    try:
        owner = await Order.get(int(message.text))
        await state.set_state(GetOrder.id)
        await message.answer(await order_from_user(owner), parse_mode="HTML",
                             reply_markup=payment_true(owner.payment, owner.id))
    except:
        await message.answer("Bunday idli buyurtma yo'q")
    await state.clear()


@user_router.callback_query(F.data.startswith('payment_'))
async def count_book(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    if data[1] == "False":
        try:
            await call.message.delete()
            await Order.update(int(data[-1]), payment=True, debt=0)
            await call.message.answer("To'lov qilindi")
        except:
            await call.message.answer("Xatolik yuz berdi")
    else:
        await call.message.answer(f"Oldin to'lov qilgan")
