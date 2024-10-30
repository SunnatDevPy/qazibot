from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from bot.buttuns.inline import confirm_order_in_group, yolda, bordi, get_order_me
from bot.detail_text import detail_text_order, order_detail
from db import Order, OrderConfirmation

group_router = Router()


class ChangeOrderState(StatesGroup):
    sum = State()
    count = State()


class NakladnoyOrderState(StatesGroup):
    photo = State()
    count = State()


# get_order_me()
@group_router.callback_query(F.data.startswith("group_"))
async def group_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = call.data.split('_')
    await call.answer()
    order = await Order.get(int(data[-1]))
    await state.update_data(order_id_in_group=data[-1])
    if data[1] == 'change':
        await call.message.delete()
        await state.set_state(ChangeOrderState.sum)
        await call.message.answer(f"{order.id}) Buyurtmadagi summa: {order.total}\nYangi narx kiriting!")
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=None)
    elif data[1] == 'confirm':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=None)
        await call.message.answer("Buyurtma qabul qilindi")
        await state.set_state(NakladnoyOrderState.photo)
        await call.message.answer("Nakladnoy yuboring")
        order_text = await detail_text_order(int(data[-1]))
        if order.delivery == "🏃Olib ketish🏃":
            pass
        else:
            send_message = await bot.send_message(-1002460328299, order_text[0], parse_mode='HTML',
                                                  reply_markup=yolda(int(data[-1])))
            await bot.send_location(-1002460328299, order_text[-1], order_text[1],
                                    reply_to_message_id=send_message.message_id)


@group_router.callback_query(F.data.startswith("get_order"))
async def group_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = call.data.split('_')
    confirmation_order = await OrderConfirmation.get_confirm_order(call.from_user.id, int(data[-1]))
    if confirmation_order is None:
        await OrderConfirmation.create(user_id=call.from_user.id, order_id=int(data[-1]))
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             reply_markup=await confirm_order_in_group(int(data[-1])))
    else:
        await call.message.answer(f"Boshqa buyurtma oling")


@group_router.message(NakladnoyOrderState.photo)
async def group_handler(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    order = data.get("order_id_in_group")
    if message.photo:
        order = await Order.get(int(order))
        await Order.update(order.id, nakladnoy=message.photo[-1].file_id)
        await bot.send_photo(order.user_id, photo=message.photo[-1].file_id,
                             caption=f"Buyurtmangiz yig'ilvotdi\nRaqami: {order.id}")
        await message.answer("Buyurtmachiga yuborildi")
        await state.clear()
    else:
        await message.answer("Ma'lumot rasim e'mas")


@group_router.callback_query(F.data.startswith("delivery_"))
async def group_handler(call: CallbackQuery, bot: Bot):
    data = call.data.split('_')
    order = await Order.get(int(data[-1]))
    if data[1] == 'start':
        await bot.send_message(order.user_id, text="Buyurtmangiz yo'lga chiqdi")
        await call.message.edit_reply_markup(call.inline_message_id, reply_markup=bordi(int(data[-1])))
    elif data[1] == 'compleat':
        await bot.send_message(order.user_id, text="Buyurtmangiz yetib keldi")
        await call.message.edit_reply_markup(call.inline_message_id, reply_markup=None)


# -1002460328299 -> yetkazish
@group_router.message(ChangeOrderState.sum)
async def group_handler(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if message.text.isdigit():
        await message.delete()
        summa = int(message.text)
        await Order.update(int(data.get('order_id_in_group')), debt=summa, total=summa)
        order = await Order.get(int(data.get('order_id_in_group')))
        text = await order_detail(order)
        await message.answer(text[0], reply_markup=await confirm_order_in_group(order.id), parse_mode="HTML")
        await state.clear()
    else:
        await message.answer("Iltimos son kiriting")

# order_detail()

# @group_router.callback_query(F.data.startswith("change_group"))
# async def group_handler(call: CallbackQuery, bot: Bot):
#     data = call.data.split('_')
#     await call.answer()
#     if data[2] == 'delete':
#         pass
#     elif data[2] == 'deleteorder':
#         await call.message.delete()
#         print(data[-1])
#         await Order.delete(int(data[-1]))
#         await call.message.answer(f"{int(data[-1])} sonli buyurtma o'chirildi")
#     elif data[2] == 'confirm':
#         order = await Order.get(int(data[-1]))
#         await call.message.edit_reply_markup(call.inline_message_id, reply_markup=None)
#         if order.delivery == '🚕Yetkazib berish🚕':
#             order_text = await detail_text_order(int(data[-1]))
#             await bot.send_message(-4563771246, order_text[0], parse_mode='HTML')
#             await bot.send_location(-4563771246, order_text[-1], order_text[1])
