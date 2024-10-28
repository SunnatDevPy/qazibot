from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.buttuns.inline import inl_categories, inl_products
from bot.buttuns.simple import menu_button, cart_from_users
from db import User

categories_router = Router()


@categories_router.message(F.text == '◀️Ortga')
async def settings(message: Message, state: FSMContext):
    if message.from_user.id in [5649321700, 279361769] + [i.id for i in await User.get_admins()]:
        await message.answer(f'Bosh menu',
                             reply_markup=await menu_button(admin=True, user_id=message.from_user.id))
    else:
        await message.answer('Bosh menu', reply_markup=await menu_button(admin=False, user_id=message.from_user.id))
    await state.clear()


@categories_router.message(F.text == "⬅️Ortga")
async def settings(message: Message, state: FSMContext):
    await message.answer("⬅️Ortga", reply_markup=await cart_from_users(user_id=message.from_user.id))
    await message.answer(html.bold('Kategoriyalardan birini tanlang!'), parse_mode="HTML",
                         reply_markup=await inl_categories())
    await state.clear()


@categories_router.message(F.text == '📖 Menu 📖')
async def categories_handler(message: Message):
    await message.answer("Menu", reply_markup=await cart_from_users(user_id=message.from_user.id))
    await message.answer(html.bold('Kategoriyalardan birini tanlang: '), reply_markup=await inl_categories(),
                         parse_mode="HTML")


@categories_router.callback_query(F.data.startswith('categories_'))
async def book_callback(call: CallbackQuery, state: FSMContext):
    await call.answer()
    detail = call.data.split('_')
    await state.update_data(category_id=int(detail[-1]))
    if detail[-1] == 'back':
        await call.message.delete()
        await call.message.answer(html.bold('Kategorialardan birini tanlang: '),
                                  reply_markup=await menu_button(admin=True, user_id=call.from_user.id),
                                  parse_mode="HTML")
    else:
        await call.message.edit_text(html.bold("Mahsulotni tanlang: "),
                                     reply_markup=await inl_products(int(detail[-1])),
                                     parse_mode="HTML")
