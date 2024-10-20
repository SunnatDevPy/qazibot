from aiogram import Router

from bot.handlers.private.admin import admin_router
from bot.handlers.private.categories_handler import categories_router
from bot.handlers.private.debt import debt_router
from bot.handlers.private.group import group_router
from bot.handlers.private.order_count import order_router
from bot.handlers.private.products import product_router
from bot.handlers.private.reklama import reklama_handler
from bot.handlers.private.start import start_router
from bot.handlers.private.user import user_router

private_handler_router = Router()

private_handler_router.include_routers(
    admin_router,
    start_router,
    categories_router,
    user_router,
    order_router,
    product_router,
    group_router,
    reklama_handler,
    debt_router,
)
