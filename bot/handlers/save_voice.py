from aiogram.enums import ContentType

SAVE_PATH = 'voice_messages/'

# Убедись, что папка для сохранения голосовых сообщений существует
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)


# Обработчик голосовых сообщений
@dp.message(content_types=ContentType.VOICE)
async def handle_voice_message(message: types.Message):
    # Получаем файл голосового сообщения
    voice = message.voice

    # Получаем файл через File API Telegram
    file_info = await bot.get_file(voice.file_id)

    # Определяем путь для сохранения
    file_name = f"{SAVE_PATH}voice_{message.from_user.id}_{voice.file_id}.ogg"

    # Скачиваем файл
    await bot.download_file(file_info.file_path, file_name)

    await message.reply("Голосовое сообщение сохранено.")