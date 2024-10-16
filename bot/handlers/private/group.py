from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.buttuns.inline import change_order_in_group
from bot.detail_text import detail_text_order, order_detail
from db import OrderItems, Order, Product

group_router = Router()


@group_router.callback_query(F.data.startswith("group_"))
async def group_handler(call: CallbackQuery, bot: Bot):
    data = call.data.split('_')
    await call.answer()
    if data[1] == 'change':
        order_text = await order_detail(int(data[-1]))
        await call.message.edit_text(order_text[0],
                                     reply_markup=await change_order_in_group(int(data[-1])))
    elif data[1] == 'confirm':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=None)
        await call.message.answer("Buyurtma qabul qilindi")
        order_text = await detail_text_order(int(data[-1]))
        await bot.send_message(-4563771246, order_text[0], parse_mode='HTML')
        await bot.send_location(-4563771246, order_text[-1], order_text[1])


# order_detail()

@group_router.callback_query(F.data.startswith("change_group"))
async def group_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = call.data.split('_')
    await call.answer()
    if data[2] == 'delete':
        order_item = await OrderItems.get(int(data[-1]))
        orderItems = await OrderItems.get_order_items(order_item.order_id)
        if len(orderItems) != 1:
            await OrderItems.delete(int(data[-1]))
            product = await Product.get(order_item.product_id)
            orders = await Order.get(order_item.order_id)
            text = await order_detail(orders)
            await Order.update(orders.id, total=orders.total - product.price)
            await call.message.edit_text(text[0], reply_markup=await change_order_in_group(int(orders.id)))
        else:
            await call.message.answer("Yagon buyurtmani o'chirolmaysiz!")
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
