from aiogram import Router, F, html, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from bot.buttuns.inline import confirm_inl, link
from bot.buttuns.simple import announce, menu_button
from db import User

reklama_handler = Router()


class SendTextState(StatesGroup):
    text = State()
    video = State()
    link = State()


class SimpleState(StatesGroup):
    text = State()
    confirm = State()


@reklama_handler.message(F.text.startswith("Reklama"))
async def count_book(message: Message):
    await message.answer("Yuborish turini tanlang", reply_markup=announce())


@reklama_handler.message(F.text == "Oddiy Xabar")
async def count_book(message: Message, state: FSMContext):
    await state.set_state(SimpleState.text)
    await message.answer("Xabar kiriting", reply_markup=ReplyKeyboardRemove())


@reklama_handler.message(SimpleState.text)
async def count_book(message: Message, state: FSMContext):
    await state.set_state(SimpleState.text)
    await state.update_data(text=message.text)
    await message.answer(message.text, reply_markup=confirm_inl())


@reklama_handler.message(F.text.in_(["Rasm-Video Xabar", "Xabar", "Oddiy xabar"]))
async def count_book(message: Message, state: FSMContext):
    text = message.text
    await state.set_state(SendTextState.text)
    if text.startswith('Rasm-Video'):
        await state.update_data(xabar='Xabar')
        await message.answer("Rasim yoki Video kiriting", reply_markup=ReplyKeyboardRemove())
    elif text.startswith('Xabar'):
        await message.answer("Xabar kiriting", reply_markup=ReplyKeyboardRemove())


@reklama_handler.message(SendTextState.text)
async def leagues_handler(msg: Message, state: FSMContext):
    if msg.photo:
        await state.set_state(SendTextState.video)
        await state.update_data(photo=msg.photo[-1].file_id)
        await msg.answer('Text xabarni kiriting', reply_markup=ReplyKeyboardRemove())
    elif msg.video:
        await state.set_state(SendTextState.video)
        await state.update_data(video=msg.video.file_id)
        await msg.answer('Text xabarni kiriting', reply_markup=ReplyKeyboardRemove())
    elif msg.text:
        await state.set_state(SendTextState.link)
        await state.update_data(text=msg.text)
        await msg.answer("Link jo'nating", reply_markup=ReplyKeyboardRemove())


@reklama_handler.message(SendTextState.video)
async def leagues_handler(msg: Message, state: FSMContext):
    await state.update_data(text=msg.text)
    await state.set_state(SendTextState.link)
    await msg.answer("Link jo'nating", reply_markup=ReplyKeyboardRemove())


@reklama_handler.message(SendTextState.link)
async def leagues_handler(msg: Message, state: FSMContext):
    await state.update_data(link=msg.text)
    data = await state.get_data()
    if len(data) == 2:
        await msg.answer(data['text'] + f'\n\n{data["link"]}', reply_markup=confirm_inl())
    else:
        if data.get('photo'):
            await msg.answer_photo(data['photo'], data['text'] + f'\n\n{data["link"]}', parse_mode='HTML',
                                   reply_markup=confirm_inl())
        else:
            await msg.answer_video(video=data['video'], caption=data['text'] + f'\n\n{data["link"]}', parse_mode='HTML',
                                   reply_markup=confirm_inl())


@reklama_handler.callback_query(F.data.endswith("_network"))
async def leagues_handler(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')
    res = await state.get_data()
    print(res)
    await call.answer()
    users: list[User] = await User.get_all()
    if data[0] == 'confirm':
        send = 0
        block = 0
        if len(res) == 2:
            for i in users:
                try:
                    await bot.send_message(i.id, res['text'], parse_mode='HTML', reply_markup=link(res['link']))
                    send += 1
                except:
                    block += 1
        elif len(res) == 1:
            for i in users:
                try:
                    await bot.send_message(i.id, res['text'], parse_mode='HTML')
                    send += 1
                except:
                    block += 1
        else:
            if res.get('photo'):
                for i in users:
                    try:
                        await bot.send_photo(chat_id=i.id, photo=res['photo'], caption=res['text'], parse_mode='HTML',
                                             reply_markup=link(res['link']))
                        send += 1
                    except:
                        block += 1
            elif res.get('video'):
                for i in users:
                    try:
                        await bot.send_video(chat_id=i.id, video=res['video'], caption=res['text'], parse_mode='HTML',
                                             reply_markup=link(res['link']))
                        send += 1
                    except:
                        block += 1
        await call.message.answer(f'Yuborildi: {send}\nBlockda: {block}')
        await call.message.answer("Bosh menu", reply_markup=await menu_button(admin=True, user_id=call.from_user.id))

    elif data[0] == 'cancel':
        await call.message.delete()
        await call.message.answer("Protsess to'xtatildi")
    await state.clear()
