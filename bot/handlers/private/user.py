from aiogram import Router, F, html, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from bot.buttuns.inline import admins, payment_true, qayta_buyurish, confirm_order_in_group
from bot.buttuns.simple import get_contact, get_location, change_user_btn, admin_panel, order_in_user, menu_button
from bot.detail_text import register_detail, order_from_user, info_orders_from_user, info_orders_from_admin, \
    order_detail
from db import User, OrderItems
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
    await state.update_data(text=text)
    if text == "Ism":
        await message.answer("Ismingizni kiriting", reply_markup=ReplyKeyboardRemove())
    elif text == "Contact":
        await message.answer("Contactingizni kiriting", reply_markup=get_contact())
    elif text == "Locatsiya":
        await message.answer("Locatsiyangizni kiriting", reply_markup=get_location())


@user_router.message(ChangeUserState.type)
async def count_book(message: Message, state: FSMContext):
    data = await state.get_data()
    user = await User.get(message.from_user.id)
    if data.get('text') == "Contact":
        if message.contact:
            await User.update(message.from_user.id, contact=message.contact.phone_number)
            await message.answer(html.bold("Telefon raqam o'zgardi"), reply_markup=ReplyKeyboardRemove(),
                                 parse_mode="HTML")
        else:
            try:
                contact = int(message.text[1:])
                await User.update(message.from_user.id, contact=message.text)
                await message.answer(html.bold("Telefon raqam o'zgardi"), reply_markup=ReplyKeyboardRemove(),
                                     parse_mode="HTML")
            except:
                await message.answer(html.bold("Telefon raqamni tog'ri kiriting"), parse_mode="HTML")

    elif message.location and data.get('text') == "Locatsiya":
        await User.update(message.from_user.id, long=message.location.longitude, lat=message.location.latitude)
        await message.answer("Locatsiyangiz o'zgardi")
    elif data.get('text') == "Ism":
        await User.update(message.from_user.id, full_name=message.text)
        await message.answer("Ismingiz o'zgardi")
    else:
        await message.answer("Ma'lumot o'zgartirishda hatolik yuz berdi")
    await message.answer(
        register_detail(message, {"full_name": user.full_name, "contact": user.contact, "idora": user.idora}),
        parse_mode='HTML', reply_markup=change_user_btn())
    await state.clear()


@user_router.message(F.text == '📃Buyurtmalarim📃')
async def count_book(message: Message):
    text = await info_orders_from_user(message.from_user.id)
    await message.answer(text, parse_mode='HTML')
    await message.answer("Tanlang", reply_markup=order_in_user())


@user_router.message(F.text.in_(["Nakladnoy", "To’lanmagan"]))
async def count_book(message: Message):
    owner = await Order.get_from_user(message.from_user.id)
    if owner:
        if message.text == "Nakladnoy":
            for i in owner:
                try:
                    await message.answer_photo(photo=i.nakladnoy, caption=f"Buyurtma soni: {i.id}", parse_mode="HTML",
                                               reply_markup=qayta_buyurish(i.id))
                except:
                    print("Hatolik")
        else:
            for i in owner:
                if i.payment == False:
                    await message.answer(await order_from_user(i), parse_mode="HTML", reply_markup=qayta_buyurish(i.id))
    else:
        await message.answer("Siz hali buyurtma qilmadingiz")


@user_router.callback_query(F.data.startswith('qayta_'))
async def count_book(call: CallbackQuery, bot: Bot):
    data = call.data.split('_')
    order = await Order.get(int(data[-1]))
    new_order = await Order.create(user_id=call.from_user.id, debt=order.total, payment=False,
                                   time=order.time,
                                   debt_type=order.debt_type, total=order.total,
                                   delivery=order.delivery)
    for i in await OrderItems.get_order_items(order.id):
        await OrderItems.create(product_id=i.product_id, count=i.count, order_id=order.id)
    text = await order_detail(new_order)
    await call.message.answer("Buyurtmangiz qabul qilindi tez orada aloqaga chiqamiz!",
                              reply_markup=await menu_button(admin=False, user_id=call.from_user.id))
    if new_order.delivery == '🏃Olib ketish🏃':
        await call.message.answer_location(latitude=41.342221, longitude=69.275769)
        await call.message.answer("Bizning manzil, QaziSay")
    await bot.send_message(-1002455618820, text[0], parse_mode="HTML",
                           reply_markup=await confirm_order_in_group(order.id))


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


@user_router.message(F.text == 'Statistika')
async def count_book(message: Message, state: FSMContext):
    text = await info_orders_from_admin()
    await message.answer(text, reply_markup=admin_panel(), parse_mode="HTML")


@user_router.message(F.text == "Admin qo'shish")
async def count_book(message: Message):
    if message.from_user.id in [5649321700, 279361769] + [i.id for i in await User.get_admins()]:
        await message.answer(html.bold("Adminlar ro'yxati"), parse_mode='HTML', reply_markup=await admins())
    else:
        await message.answer(f"Sizda huquq yo'q")


@user_router.message(F.text == "To'lanmagan buyurtmalar")
async def count_book(message: Message):
    if message.from_user.id in [5649321700, 279361769] + [i.id for i in await User.get_admins()]:
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
