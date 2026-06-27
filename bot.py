import asyncio
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

# ---------------------
# تنظیمات
# ---------------------

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

FILTERED_WORDS = [
    "میو",
    "ماهی",
    "spam"
]

# ---------------------
# لاگ
# ---------------------

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

# ---------------------
# حذف پیام
# ---------------------

async def delete_after_delay(message, seconds: int):
    await asyncio.sleep(seconds)

    try:
        await message.delete()
        print("🗑 پیام حذف شد")

    except Exception as e:
        print("خطا در حذف:", e)

# ---------------------
# بررسی پیام
# ---------------------

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()

    print("🔥 MESSAGE:", text)

    # اگر کلمه فیلتر شده بود
    if any(word in text for word in FILTERED_WORDS):

        print("🚨 FILTERED WORD DETECTED")

        asyncio.create_task(
            delete_after_delay(
                update.message,
                20  # زمان حذف (ثانیه)
            )
        )

# ---------------------
# اجرا
# ---------------------

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_message)
    )

    print("🤖 BOT STARTED")

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()