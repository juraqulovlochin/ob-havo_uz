import requests
import asyncio
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
load_dotenv()
Token = getenv("BOT_TOKEN")
bot = Bot(token=Token)
dp = Dispatcher()

tugmalar = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Tashkent")],
        [KeyboardButton(text="Samarkand"), KeyboardButton(text="Andijan")],
        [KeyboardButton(text="Bukhara"), KeyboardButton(text="Fergana")],
        [KeyboardButton(text="Namangan"), KeyboardButton(text="Navoi")],
        [KeyboardButton(text="Karshi"), KeyboardButton(text="Termez")],
        [KeyboardButton(text="Gulistan"), KeyboardButton(text="Nukus")],
        [KeyboardButton(text="Jizzakh")]
    ],
    resize_keyboard=True
)

@dp.message(Command('start'))
async def starthandler(message: types.Message):
    await message.reply("Xush kelibsiz!\nJoylashuvni tanlang.\nBiz sizga 3 kunlik ob-havo ma'lumotini taqdim etamiz.",reply_markup=tugmalar)

@dp.message(Command('help'))
async def helphandler(message: types.Message):
    await message.reply("Botdan foydalanish uchun shahar nomini kiriting. Biz sizga 3 kunlik ob-havo ma'lumotini taqdim etamiz.",reply_markup=tugmalar)

@dp.message()
async def malumot(message: types.Message):
    key =getenv("WEATHER_API_KEY")
    shahar = message.text.strip()
    url = "http://api.weatherapi.com/v1/forecast.json"
    parametr = {
        'key': key,
        'q': shahar,
        'lang': 'uz',
        'days': 3
    }

    try:
        response = requests.get(url, params=parametr, timeout=5)
        data = response.json()

        if "error" in data:
            return await message.reply("❌ Shahar topilmadi. Iltimos, nomini to‘g‘ri kiriting.")

        def emoji_holat(text):
            txt = text.lower()
            if "sunny" in txt or "clear" in txt:
                return "☀️"
            elif "partly" in txt:
                return "🌤"
            elif "cloud" in txt:
                return "☁️"
            elif "mist" in txt or "fog" in txt:
                return "🌫"
            elif "rain" in txt or "drizzle" in txt:
                return "🌧"
            elif "thunder" in txt or "storm" in txt:
                return "⛈"
            elif "snow" in txt:
                return "❄️"
            elif "sleet" in txt:
                return "🌨"
            elif "overcast" in txt:
                return "🌥"
            else:
                return "🌈"

        from datetime import datetime

        def uzbek_hafta_kuni(date_str):

            hafta_kunlari = {
                "Monday": "Dushanba",
                "Tuesday": "Seshanba",
                "Wednesday": "Chorshanba",
                "Thursday": "Payshanba",
                "Friday": "Juma",
                "Saturday": "Shanba",
                "Sunday": "Yakshanba"
            }
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            hafta_kuni = dt.strftime("%A")
            uz_kun = hafta_kunlari.get(hafta_kuni, hafta_kuni)

            return dt.strftime(f"%d-%m-%Y ({uz_kun})")

        for kun in data['forecast']['forecastday']:
            sana = uzbek_hafta_kuni(kun['date'])
            holat_matn = kun['day']['condition']['text']
            emoji = emoji_holat(holat_matn)


            holat = "Nomalum"
            if "clear" in holat_matn.lower() or "sunny" in holat_matn.lower():
                holat = "Ochiq osmon. Quyoshli"
            elif "partly" in holat_matn.lower():
                holat = "Qisman bulutli"
            elif "cloud" in holat_matn.lower():
                holat = "Bulutli"
            elif "mist" in holat_matn.lower() or "fog" in holat_matn.lower():
                holat = "Tumanli"
            elif "light rain" in holat_matn.lower():
                holat = "Hafif yomg‘ir"
            elif "rain" in holat_matn.lower():
                holat = "Yomg‘irli"
            elif "thunder" in holat_matn.lower():
                holat = "Momaqaldiroq"
            elif "snow" in holat_matn.lower():
                holat = "Qorli"
            elif "sleet" in holat_matn.lower():
                holat = "Qor-yomg‘ir aralash"

            min_temp = kun['day']['mintemp_c']
            max_temp = kun['day']['maxtemp_c']
            avg_humid = kun['day']['avghumidity']
            max_wind = round(kun['day']['maxwind_kph'] / 3.6, 2)  # m/s

            matn = (
                f"📅 *{sana}* — *{shahar.title()}*\n"
                f"🌡 Harorat: {min_temp}°C — {max_temp}°C\n"
                f"{emoji} *Holat:* {holat} \n"
                f"💧 Namlik: {avg_humid}%\n"
                f"💨 Shamol: {max_wind} m/s"
            )

            await message.reply(matn, parse_mode="Markdown")


    except Exception as e:
        await message.reply("⚠️ Ob-havo ma'lumotlarini olishda xatolik yuz berdi.")
        print(f"[Xato] {e}")


async def boshlash():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(boshlash())
