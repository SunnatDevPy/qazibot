import pandas as pd
from aiogram import Router, html, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from bot.buttuns.inline import admins
from bot.buttuns.simple import cancel_excel, admin_panel
from db import User, Categorie, Product

admin_router = Router()


class AddAdmin(StatesGroup):
    user_id = State()


class ExcelImportState(StatesGroup):
    file_id = State()


@admin_router.message(F.text.startswith("Excel"))
async def count_book(message: Message, state: FSMContext):
    text = message.text.replace("Excel ", '')
    print(text)
    if message.from_user.id in [5649321700, 279361769] + [i for i in await User.get_admins()]:
        await state.set_state(ExcelImportState.file_id)
        if text == 'kategoriya':
            await message.answer("Kategoriyaga tegishli excel fayl yuboring!", reply_markup=cancel_excel())
            await message.answer("Qatorlar ketma ketligi: \n1) id[1-9], \n2) title[salom, world]!")
        elif text == 'mahsulot':
            await message.answer("Mahxulotga tegishli excel fayl yuboring!", reply_markup=cancel_excel())
            await message.answer(
                "Qatorlar ketma ketligi: \n1) id[1-10000], \n2) category_id[1-1000], \n3) photo[link] bo'lmasa bosh qoldiring, \n4) title[salom], \n5) restoran_price[12000],\n6) optom_price[12000], \n7) type[dona/kg],\n8) description[zo'r mahsulot]: qo'shimcha ma'lumot!")
    else:
        await message.answer(f"Sizda huquq yo'q")


@admin_router.message(ExcelImportState.file_id)
async def count_book(message: Message, state: FSMContext, bot: Bot):
    if message.text == "❌":
        await state.clear()
        await message.answer("Admin panel", reply_markup=admin_panel())
    else:
        file_info = await bot.get_file(message.document.file_id)

        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)
        with open("data.xlsx", "wb") as new_file:
            new_file.write(downloaded_file.getvalue())
        df = pd.read_excel('data.xlsx')
        text = ''
        brak = 0
        await message.answer("Bir oz kuting...", reply_markup=ReplyKeyboardRemove())
        for index, row in df.iterrows():
            print(row)

            if row.get('category_id'):
                try:
                    await Product.create(id=row['id'], category_id=row['category_id'], photo=row['photo'],
                                         title=row['title'], restoran_price=row["restoran_price"],
                                         optom_price=row["optom_price"], type=row['type'],
                                         description=row['description'])
                except:
                    await Product.create(id=row['id'], category_id=row['category_id'], photo=None,
                                         title=row['title'], type=row['type'],
                                         description=row['description'], restoran_price=row["restoran_price"],
                                         optom_price=row["optom_price"], )
            else:
                await Categorie.create(id=row['id'], title=row['title'])

                brak += 1
                text += f'{row["id"]}, '
        else:
            if brak != 0:
                await message.answer(text + "idlar zaynit", reply_markup=admin_panel())
            else:
                await message.answer("Muvoffaqiyatli yuklandi", reply_markup=admin_panel())
        await state.clear()


@admin_router.callback_query(F.data.startswith('admins_'))
async def delete_admins(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    await call.answer()
    if data[1] == 'add':
        await call.message.delete()
        await state.set_state(AddAdmin.user_id)
        await call.message.answer(html.bold("User idni kiriting"), parse_mode='HTML')
    if data[1] == 'delete':
        try:
            await User.update(id_=int(data[-1]), is_admin=False)
            await call.message.edit_text(html.bold("Adminlar ro'yxati"), parse_mode='HTML', reply_markup=await admins())
        except:
            await call.message.answer('Xatolik yuz berdi')


@admin_router.message(AddAdmin.user_id)
async def add_admin(call: Message):
    try:
        user = await User.get(int(call.text))
        if user:
            text = html.bold(f'''
#Admin qo'shildi
chat_id: <code>{user.id}</code>
Username: <code>@{user.username}</code>
                ''')
            await User.update(id_=user.id, is_admin=True)
            await call.answer(text, parse_mode='HTML')
            await call.answer(html.bold("Adminlar ro'yxati"), parse_mode='HTML', reply_markup=await admins())
        else:
            await call.answer(html.bold("Bunaqa id li user yo'q, bo'tga /start bergan bo'lish kerak"),
                              parse_mode='HTML')
    except:
        await call.answer(html.bold("Id kiritmadingiz"), parse_mode='HTML')
