import asyncio
import logging
import os
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

BOT_TOKEN = os.getenv("BOT_TOKEN")

# فقط ID رباتی که می‌خوای حذف بشه
TARGET_BOT_ID = 8024943840  # <-- اینجا آی‌دی ربات رو بذار

FILTERED_WORDS = [
    "میو",
    "ماهی",
    "پیشی"
    "میوهام"
    "میوهاش"
    "معو"
    "انتقال میویی"
    "پیشی"
    

]

# ---------------------
# لاگ
# ---------------------

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

# ---------------------
# حذف پیام با تأخیر
# ---------------------

async def delete_after_delay(message, seconds: int):
    await asyncio.sleep(seconds)

    try:
        await message.delete()
        print("🗑 پیام حذف شد")

    except Exception as e:
        print("❌ خطا در حذف:", e)

# ---------------------
# بررسی پیام‌ها
# ---------------------

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    text = (update.message.text or "").lower()
    user = update.message.from_user

    print("🔥 MESSAGE:", text)

    should_delete = False

    # 1) پیام از ربات خاص
    if user and user.is_bot and user.id == TARGET_BOT_ID:
        print("🤖 پیام از ربات هدف شناسایی شد")
        should_delete = True

    # 2) پیام دارای کلمات فیلتر شده
    if any(word in text for word in FILTERED_WORDS):
        print("🚨 کلمه فیلتر شده پیدا شد")
        should_delete = True

    # اگر باید حذف شود
    if should_delete:
        asyncio.create_task(
            delete_after_delay(update.message, 60)
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
