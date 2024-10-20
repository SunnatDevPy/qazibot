from aiogram import Router, F, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from bot.detail_text import detail_text_order
from db import Order

group_router = Router()


class ChangeOrderState(StatesGroup):
    sum = State()
    count = State()


@group_router.callback_query(F.data.startswith("group_"))
async def group_handler(call: CallbackQuery, bot: Bot):
    data = call.data.split('_')
    await call.answer()
    if data[1] == 'change':
        await call.message.answer("Summa kiriting")
        pass
    elif data[1] == 'confirm':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=None)
        await call.message.answer("Buyurtma qabul qilindi")
        order_text = await detail_text_order(int(data[-1]))
        send_message = await bot.send_message(-4563771246, order_text[0], parse_mode='HTML')
        await bot.send_location(-4563771246, order_text[-1], order_text[1], reply_to_message_id=send_message.message_id)


# order_detail()

@group_router.callback_query(F.data.startswith("change_group"))
async def group_handler(call: CallbackQuery, bot: Bot):
    data = call.data.split('_')
    await call.answer()
    if data[2] == 'delete':
        pass
    elif data[2] == 'deleteorder':
        await call.message.delete()
        print(data[-1])
        await Order.delete(int(data[-1]))
        await call.message.answer(f"{int(data[-1])} sonli buyurtma o'chirildi")
    elif data[2] == 'confirm':
        order = await Order.get(int(data[-1]))
        await call.message.edit_reply_markup(call.inline_message_id, reply_markup=None)
        if order.delivery == '🚕Yetkazib berish🚕':
            order_text = await detail_text_order(int(data[-1]))
            await bot.send_message(-4563771246, order_text[0], parse_mode='HTML')
            await bot.send_location(-4563771246, order_text[-1], order_text[1])
