from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def menu_button(admin):
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text='📖 Menu 📖'),
             KeyboardButton(text="👤Mening ma'lumotlarim👤"),
             KeyboardButton(text='📃Buyurtmalarim📃'),
             KeyboardButton(text=f"🛒Savat"),
             KeyboardButton(text='📝Qoldiq'),
             KeyboardButton(text='Do\'kon haqida')
             ])
    if admin == True:
        kb.add(*[
            KeyboardButton(text='Settings')
        ])
    kb.adjust(1, 1, 2, 2)
    return kb.as_markup(resize_keyboard=True)


def admin_panel():
    kb = ReplyKeyboardBuilder()
    kb.add(*[
        KeyboardButton(text='Userlar soni'),
        KeyboardButton(text="Admin qo'shish"),
        KeyboardButton(text="To'lanmagan buyurtmalar"),
        KeyboardButton(text="Id bo'yicha buyurtma"),
        KeyboardButton(text="Excel kategoriya"),
        KeyboardButton(text="Excel mahsulot"),
        KeyboardButton(text="Reklama"),
        KeyboardButton(text="◀️Ortga")
    ])
    kb.adjust(2, 2)
    return kb.as_markup(resize_keyboard=True)


def announce():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text="Rasm-Video Xabar"),
             KeyboardButton(text="Xabar"),
             KeyboardButton(text="Oddiy Xabar"),
             KeyboardButton(text="◀️Ortga")])
    kb.adjust(1, 2, 1)
    return kb.as_markup(resize_keyboard=True)


def change_user_btn():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text="Ism-familiya"),
             KeyboardButton(text="Contact"),
             KeyboardButton(text="Locatsiya"),
             KeyboardButton(text="◀️Ortga")])
    kb.adjust(2, 2)
    return kb.as_markup(resize_keyboard=True)


def cart_from_users(order=0):
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text=f"🛒Savat"), KeyboardButton(text="◀️Ortga")])
    return kb.as_markup(resize_keyboard=True)


def group_confirm():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text="✅QABUL QILDIM✅")])
    return kb.as_markup(resize_keyboard=True)


def cancel_excel():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text="❌")])
    return kb.as_markup(resize_keyboard=True)


def get_contact():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text='📞Contact jonatish📞', request_contact=True)])
    return kb.as_markup(resize_keyboard=True)


def detail_delivery():
    kb = ReplyKeyboardBuilder()
    kb.add(*[
        KeyboardButton(text='🚕Yetkazib berish🚕'),
        KeyboardButton(text='🏃Olib ketish🏃')
    ])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def choose_payment():
    kb = ReplyKeyboardBuilder()
    kb.add(*[
        KeyboardButton(text='Qarzga'),
        KeyboardButton(text='Naxtga')
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
