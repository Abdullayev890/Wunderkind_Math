import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message

# Tokeningiz
BOT_TOKEN = "9102809407:AAFYeQ_T1chXf0j1iD5a_uw3RlhcCTHjsrs"

# Hozircha bo'sh kalitlar lug'ati (keyin o'zgartirishingiz mumkin)
TEST_KEYS = {
    1: "ACBDCABDCBADBCABD",
    2: "ABCDABCDABCDABCD"
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "👋 **Salom! Test javoblarini tekshirish botiga xush kelibsiz.**\n\n"
        "Javoblaringizni quyidagi formatda yuboring:\n"
        "`TestRaqami*Javoblaringiz`\n\n"
        "**Misol uchun:** `1*ACBDCABDCBADBCABD`"
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text.contains("*"))
async def check_answers_handler(message: Message):
    try:
        parts = message.text.strip().split("*")
        if len(parts) != 2 or not parts[0].isdigit():
            await message.answer("⚠️ Xato format! Iltimos, `1*ABCD...` shaklida yuboring.")
            return

        test_id = int(parts[0])
        user_answers = parts[1].upper().replace(" ", "")

        if test_id not in TEST_KEYS:
            await message.answer(f"❌ **{test_id}-sonli test topilmadi!**")
            return

        correct_answers = TEST_KEYS[test_id].upper()
        total_questions = len(correct_answers)

        correct_count = 0
        wrong_count = 0

        for i in range(min(len(user_answers), total_questions)):
            if user_answers[i] == correct_answers[i]:
                correct_count += 1
            else:
                wrong_count += 1

        percentage = round((correct_count / total_questions) * 100, 1)

        result_text = (
            f"📊 **Test Natijasi:**\n\n"
            f"🔹 **Test raqami:** {test_id}\n"
            f"🔹 **Jami savollar:** {total_questions} ta\n"
            f"✅ **To'g'ri javoblar:** {correct_count} ta\n"
            f"❌ **Noto'g'ri javoblar:** {wrong_count} ta\n\n"
            f"📈 **Natija:** {percentage}%"
        )
        await message.answer(result_text, parse_mode="Markdown")
    except Exception as e:
        await message.answer("⚠️ Xatolik yuz berdi. Formatni qayta tekshiring.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
