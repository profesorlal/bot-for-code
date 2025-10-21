import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

TOKEN = "7950628886:AAGbyluSDeTwHY9y1ELkpi9RYRBDDGqlIEE"

bot = Bot(token=TOKEN)

dp = Dispatcher()

@dp.message(Command("get_code"))
async def start_cmd(msg: types.Message):
  code = requests.post("https://quizizz-answer.vercel.app/point", headers={"Content-Type":"application/json"}, json={"password":"Quizizz_Admin"}).json
  await msg.answer(code)

async def main():
  await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
