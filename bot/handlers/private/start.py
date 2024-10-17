from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, Chat

from bot.buttuns.inline import confirm_register_inl, permission_user
from bot.buttuns.simple import get_contact, get_location, menu_button
from bot.detail_text import register_detail
from config import BOT
from db import User
from state.states import Register

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    user = await User.get(message.from_user.id)
    if not user:
        await message.answer("Ro'yxatdan o'ting")
        await state.set_state(Register.full_name)
        await message.answer("Ism familiyangizni kiriting")
    else:
        if message.from_user.id in [279361769, 5649321700] + [i for i in await User.get_admins()]:
            await message.answer(f'Xush kelibsiz Admin {message.from_user.first_name}',
                                 reply_markup=menu_button(admin=True))
        else:
            await message.answer(f'Xush kelibsiz {message.from_user.first_name}',
                                 reply_markup=menu_button(admin=False))


@start_router.message(F.chat.type.in_['group', 'supergroup'])
async def command_start(message: Message):
    await message.answer("Sizda huquq yo'q", reply_markup=ReplyKeyboardRemove())


@start_router.message(Register.full_name)
async def register_full_name(msg: Message, state: FSMContext):
    await state.update_data(full_name=msg.text)
    await state.set_state(Register.contact)
    await msg.answer("📞Contact yuboring📞", reply_markup=get_contact())


@start_router.message(Register.contact)
async def register_full_name(msg: Message, state: FSMContext):
    if msg.contact:
        await state.update_data(contact=msg.contact.phone_number)
        await state.set_state(Register.idora)
        await msg.answer("Idora nomini kiriting", reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("Contact yubormadingiz, pastgi tugamni bosing", reply_markup=get_contact())


@start_router.message(Register.idora)
async def register_full_name(message: Message, state: FSMContext):
    await state.update_data(idora=message.text)
    await state.set_state(Register.location)
    await message.answer("📍Locatsiya yuboring📍", reply_markup=get_location())


@start_router.message(Register.location)
async def register_full_name(msg: Message, state: FSMContext):
    if msg.location:
        await state.update_data(long=msg.location.longitude, lat=msg.location.latitude)
        await state.set_state(Register.confirm)
        data = await state.get_data()
        await msg.answer("Ma'lumotingiz to'g'rimi?", reply_markup=ReplyKeyboardRemove())
        await msg.answer(register_detail(msg, data), parse_mode='HTML',
                         reply_markup=confirm_register_inl())
    else:
        await msg.answer("Iltimos locatsiya jo'nating")


@start_router.callback_query(Register.confirm, F.data.endswith('_register'))
async def register_full_name(call: CallbackQuery, state: FSMContext):
    confirm = call.data.split('_')
    data = await state.get_data()
    await call.message.delete()
    if confirm[0] == 'confirm':
        user_data = {'id': call.from_user.id, 'username': call.from_user.username,
                     'full_name': data.get('full_name'), "idora": data.get("idora"), "long": data.get('long'),
                     "lat": data.get('lat'), "contact": str(data.get('contact'))}
        await User.create(**user_data)
        for admin in await User.get_admins():
            await call.bot.send_message(admin.id, register_detail(call, data),
                                        reply_markup=permission_user(call.from_user.id),
                                        parse_mode="HTML")
        await call.bot.send_message(BOT.ADMIN, register_detail(call, data),
                                    reply_markup=permission_user(call.from_user.id),
                                    parse_mode="HTML")
        await call.bot.send_message(279361769, register_detail(call, data),
                                    reply_markup=permission_user(call.from_user.id),
                                    parse_mode="HTML")
        if call.from_user.id in [5649321700, 279361769] + [i for i in await User.get_admins()]:
            await call.message.answer(f'Xush kelibsiz Admin {call.from_user.first_name}',
                                      reply_markup=menu_button(admin=True))
        else:
            await call.message.answer("Ro'yxatdan o'tdingiz, tez orada adminlarimiz permission berishadi!",
                                      parse_mode='HTML')
        await state.clear()
    else:
        await state.set_state(Register.full_name)
        await call.message.answer("Qayta ro'yxatdan o'ting")


@start_router.callback_query(F.data.startswith('permission_'))
async def register_full_name(call: CallbackQuery, bot: Bot):
    data = call.data.split('_')
    await call.message.delete()
    if data[1] == 'confirm':
        await call.message.answer("Ruxsat berildi")
        await bot.send_message(data[-1], 'Xush kelibsiz, bot ishlatishga ruxsat berildi',
                               reply_markup=menu_button(admin=False))
    else:
        try:
            await User.delete(int(data[-1]))
        except:
            await call.message.answer("O'chirishda xatolik")
