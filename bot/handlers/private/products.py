from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.buttuns.inline import inl_products, inl_categories
from bot.buttuns.simple import cart_from_users
from bot.detail_text import product_detail
from db import Product, User
from db.models.model import Cart
from state.states import ProductOrderState

product_router = Router()


@product_router.message(F.text == "Yana qo'shish")
async def book_callback(message: Message, state: FSMContext):
    data = await state.get_data()
    try:

        await message.answer("Ortga", reply_markup=await cart_from_users(message.from_user.id))
        await message.answer(html.bold("Mahsulotni tanlang: "),
                             reply_markup=await inl_products(int(data.get("product_id"))),
                             parse_mode="HTML")
    except:
        await message.answer(html.bold('Kategorialardan birini tanlang: '), reply_markup=await inl_categories(),
                             parse_mode="HTML")


# @product_router.callback_query(F.data.startswith('product_'))
# async def book_callback(call: CallbackQuery, state: FSMContext):
#     data = call.data.split('_')
#     # await call.message.delete()
#     if data[-1] == 'back':
#         await call.message.delete()
#         await call.message.answer(html.bold('Kategorialardan birini tanlang: '), reply_markup=await inl_categories(),
#                                   parse_mode="HTML")
#     else:
#         await call.answer()
#         product = await Product.get(int(data[-1]))
#         user = await User.get(call.from_user.id)
#         text = await product_detail(product, user)
#         try:
#             await call.message.answer_photo(text[1],
#                                             caption=text[0], parse_mode='HTML')
#         except:
#             await call.message.answer(text[0], parse_mode='HTML')
#         type = product.type
#         if type == 'dona':
#             type = "Nechi dona ? Yozing"
#         else:
#             type = "Nechi kg ? Yozing"
#
#         await state.update_data(product_id=int(data[-1]), type=type, product_name=product.title, product_price=text[-1])
#         await state.set_state(ProductOrderState.count)
#         await call.message.answer(type, reply_markup=await cart_from_users(user_id=call.from_user.id))

@product_router.callback_query(F.data.startswith('product_'))
async def book_callback(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    await call.answer()
    await call.message.delete()
    if data[-1] == 'back':
        await call.message.delete()
        await call.message.answer("Kategorialardan birini tanlang:", reply_markup=await inl_categories(),
                                  parse_mode="HTML")
    else:
        product = await Product.get(int(data[-1]))
        user = await User.get(call.from_user.id)
        text = await product_detail(product, user)

        try:
            await call.message.answer_photo(text[1], caption=text[0], parse_mode='HTML')
        except Exception:
            await call.message.answer(text[0], parse_mode='HTML')

        type = "Nechi dona? Yozing" if product.type == 'dona' else "Nechi kg? Yozing"
        await state.update_data(product_id=int(data[-1]), type=type, product_name=product.title, product_price=text[-1])
        await state.set_state(ProductOrderState.count)
        await call.message.answer(type, reply_markup=await cart_from_users(user_id=call.from_user.id))


@product_router.message(ProductOrderState.count)
async def book_callback(msg: Message, state: FSMContext):
    data = await state.get_data()
    product = await Product.get(int(data.get("product_id")))
    if msg.text == '⬅️Ortga':
        await state.clear()
        await msg.answer(html.bold("Mahsulotni tanlang: "),
                         reply_markup=await inl_products(product.category_id),
                         parse_mode="HTML")
    else:
        product_in_cart = await Cart.get_product_in_cart(msg.from_user.id, int(data.get("product_id")))

        try:
            price = float(msg.text.replace(',', '.').strip())
            if '.' in msg.text and product.type == "dona" or ',' in msg.text and product.type == "dona":
                await msg.answer(html.bold(f"Donali mahsulotga notog'ri malumot kiritdingiz!"),
                                 parse_mode="HTML")
            else:
                await state.update_data(count=price)
                if product_in_cart:
                    await Cart.update(product_in_cart.id, count=product_in_cart.count + price,
                                      total=product_in_cart.total + int(float(data.get('product_price')) * price))
                else:
                    await Cart.create(user_id=msg.from_user.id, product_id=data.get("product_id"),
                                      count=price,
                                      total=int(data.get('product_price') * price))
                await msg.answer(
                    f"Savatga qo'shildi: {data.get('product_name')}\n\nBuyurtma qilish uchun savatga o'ting!",
                    reply_markup=await cart_from_users(user_id=msg.from_user.id))
                await msg.answer(html.bold("Mahsulotni tanlang: "),
                                 reply_markup=await inl_products(product.category_id),
                                 parse_mode="HTML")
                await state.clear()
        except:
            await msg.answer(f"{msg.text} noto'g'ri")
            await msg.answer(f"Boshqa malumot yubordingiz, yoki juda kotta son")
