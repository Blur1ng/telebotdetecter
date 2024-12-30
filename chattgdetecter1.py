import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = ''

# Папки для сохранения
SAVE_FOLDER = "data"
IMAGE_FOLDER = os.path.join(SAVE_FOLDER, "/Users/evgene/Documents/python_scripts/telebot/pdimages1")

# Убедимся, что папки для сохранения существуют
os.makedirs(SAVE_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)


async def save_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    sender = update.message.from_user.first_name
    date = datetime.now().strftime("%H:%M:%S")

    log_entry = f"{message} ({sender} | {date})\n"

    filepath = f"/Users/evgene/Documents/python_scripts/telebot/pdtexts/{datetime.now().strftime("%Y-%m-%d")}.txt"
    if os.path.isfile(filepath):
        with open(filepath, "a", encoding="utf-8") as file:
            file.write(log_entry)
    else:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(log_entry)

async def save_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photos = update.message.photo
    if not photos:
        return
    # Берём фотографию с максимальным разрешением
    photo = photos[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = os.path.join(IMAGE_FOLDER, f"{photo.file_id}.jpg")
    await file.download_to_drive(file_path)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_text))
    app.add_handler(MessageHandler(filters.PHOTO, save_image))

    app.run_polling()

if __name__ == '__main__':
    main()
