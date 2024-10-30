from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.detail_text import sum_cart, change_number


async def menu_button(admin, user_id):
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text='📖 Menu 📖'),
             KeyboardButton(text='📃Buyurtmalarim📃'),
             KeyboardButton(text='📝Qoldiq'),
             KeyboardButton(text=f"🛒Savat ({change_number(await sum_cart(user_id))} so'm)"),
             KeyboardButton(text="👤Mening ma'lumotlarim👤"),
             KeyboardButton(text='Do\'kon haqida')
             ])
    if admin == True:
        kb.add(*[
            KeyboardButton(text='Settings')
        ])
    kb.adjust(1, 2, 1, 1, 2)
    return kb.as_markup(resize_keyboard=True)


# Nakladnoy | To’lanmagan

def order_in_user():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text="Nakladnoy"),
             KeyboardButton(text="To’lanmagan"),
             KeyboardButton(text="⬅️Ortga")])
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)


def admin_panel():
    kb = ReplyKeyboardBuilder()
    kb.add(*[
        KeyboardButton(text='Statistika'),
        KeyboardButton(text="Admin qo'shish"),
        KeyboardButton(text="To'lanmagan buyurtmalar"),
        KeyboardButton(text="Id bo'yicha buyurtma"),
        KeyboardButton(text="Qarzini yopish"),
        KeyboardButton(text="Excel"),
        KeyboardButton(text="Reklama"),
        KeyboardButton(text="◀️Ortga")
    ])
    kb.adjust(2, 2)
    return kb.as_markup(resize_keyboard=True)


def excel():
    kb = ReplyKeyboardBuilder()
    kb.add(*[
        KeyboardButton(text="Kategoriya kiritish"),
        KeyboardButton(text="Mahsulot kiritish"),
        KeyboardButton(text="Mahsulot o'zgartirish"),
        KeyboardButton(text="⬅️Ortga")
    ])
    kb.adjust(2, 1, 1)
    return kb.as_markup(resize_keyboard=True)


def announce():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text="Rasm-Video Xabar"),
             KeyboardButton(text="Xabar"),
             KeyboardButton(text="Oddiy Xabar"),
             KeyboardButton(text="⬅️Ortga")])
    kb.adjust(1, 2, 1)
    return kb.as_markup(resize_keyboard=True)


def change_user_btn():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text="Ism"),
             KeyboardButton(text="Contact"),
             KeyboardButton(text="Locatsiya"),
             KeyboardButton(text="◀️Ortga")])
    kb.adjust(2, 2)
    return kb.as_markup(resize_keyboard=True)


async def cart_from_users(user_id):
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text=f"🛒Savat ({change_number(await sum_cart(user_id))} so'm)"),
             KeyboardButton(text="◀️Ortga")])
    kb.adjust()
    return kb.as_markup(resize_keyboard=True)


def debt_check():
    kb = ReplyKeyboardBuilder()
    kb.row(*[KeyboardButton(text=f"Summa kiritish"), KeyboardButton(text="Barchasini yopish")])
    kb.row(*[KeyboardButton(text=f"⬅️Ortga")])
    return kb.as_markup(resize_keyboard=True)


def otkazish():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text="O'tkazib yuborish"),

             KeyboardButton(text="◀️ Ortga")])
    return kb.as_markup(resize_keyboard=True)


def cancel_excel():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text="❌")])
    return kb.as_markup(resize_keyboard=True)


def cancel_sum():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text="❌Toxtatish❌")])
    return kb.as_markup(resize_keyboard=True)


def get_contact():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text='📞Contact jonatish📞', request_contact=True)])
    return kb.as_markup(resize_keyboard=True)


def detail_delivery():
    kb = ReplyKeyboardBuilder()
    kb.add(*[
        KeyboardButton(text='🚕Yetkazib berish🚕'),
        KeyboardButton(text='🏃Olib ketish🏃'),
        KeyboardButton(text="◀️ Ortga")
    ])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def choose_payment():
    kb = ReplyKeyboardBuilder()
    kb.add(*[
        KeyboardButton(text='Qarzga'),
        KeyboardButton(text='Naxtga'),
        KeyboardButton(text="◀️Ortga")
    ])
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)


def cart_detail_btn():
    ikb = ReplyKeyboardBuilder()
    ikb.add(*[KeyboardButton(text='✅ Buyurtma qilish'),
              KeyboardButton(text='Tozalash'),
              KeyboardButton(text="Yana qo'shish"),
              KeyboardButton(text='◀️Ortga'),
              ])
    ikb.adjust(1, 2, 1)
    return ikb.as_markup(resize_keyboard=True)


def get_location():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text='📍Locatsiya jonatish📍', request_location=True)])
    return kb.as_markup(resize_keyboard=True)
