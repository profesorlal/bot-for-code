import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from aiohttp import web
import aiohttp
import json

TOKEN = "7950628886:AAGbyluSDeTwHY9y1ELkpi9RYRBDDGqlIEE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def start_cmd(msg: types.Message):
    code = requests.post("https://quizizz-answer.vercel.app/point", headers={"Content-Type":"application/json"}, json={"password":"Quizizz_Admin"}).json()["code"]
    await msg.answer(code)

# === Новый эндпоинт для AI запросов ===
async def groq_handler(request):
    try:
        # Получаем данные из запроса
        data = await request.json()
        user_message = data.get('message', '')
        
        if not user_message:
            return web.json_response({'error': 'No message provided'}, status=400)
        
        async with aiohttp.ClientSession() as session:
            # Отправляем запрос к Groq AI напрямую с токеном
            headers = {
                'accept': 'application/json',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Imp3ay1saXZlLTMyNDg5ODNiLWEzYWYtNGVlZi1iZDAyLTQ4YTEyOWU3NmIyYSIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsicHJvamVjdC1saXZlLTVjYjM4ODBlLTc3NGUtNDNlYS1hYjkwLWY0ZDMyMzRlMzZkZCJdLCJleHAiOjE3NjI0MjE5OTUsImh0dHBzOi8vZ3JvcS5jb20vb3JnYW5pemF0aW9uIjp7ImlkIjoib3JnXzAxazkyZ3ZjMGpmOG50ejgydHNjdHh5ZDEyIn0sImh0dHBzOi8vc3R5dGNoLmNvbS9vcmdhbml6YXRpb24iOnsib3JnYW5pemF0aW9uX2lkIjoib3JnYW5pemF0aW9uLWxpdmUtODBiZDczNWQtMjlkYS00NmQzLWFmYjAtNGEzMDA2MWE0NjVmIiwic2x1ZyI6Im9yZ18wMWs5Mmd2YzBqZjhudHo4MnRzY3R4eWQxMiJ9LCJodHRwczovL3N0eXRjaC5jb20vc2Vzc2lvbiI6eyJpZCI6Im1lbWJlci1zZXNzaW9uLWxpdmUtNjMwYzQ1NjYtNTE2MC00ODIzLTgxNzEtNTNjZWYyNjE5Yjc5Iiwic3RhcnRlZF9hdCI6IjIwMjUtMTEtMDZUMDk6MzQ6NTVaIiwibGFzdF9hY2Nlc3NlZF9hdCI6IjIwMjUtMTEtMDZUMDk6MzQ6NTVaIiwiZXhwaXJlc19hdCI6IjIwMjUtMTItMDZUMDk6MzQ6NTVaIiwiYXR0cmlidXRlcyI6eyJ1c2VyX2FnZW50IjoiIiwiaXBfYWRkcmVzcyI6IiJ9LCJhdXRoZW50aWNhdGlvbl9mYWN0b3JzIjpbeyJ0eXBlIjoib2F1dGgiLCJkZWxpdmVyeV9tZXRob2QiOiJvYXV0aF9nb29nbGUiLCJsYXN0X2F1dGhlbnRpY2F0ZWRfYXQiOiIyMDI1LTExLTA2VDA5OjM0OjU0WiIsImdvb2dsZV9vYXV0aF9mYWN0b3IiOnsiaWQiOiJvYXV0aC1yZWdpc3RyYXRpb24tbGl2ZS0xMDZlNjIwMC0zOWJhLTQ2NmItOTUyZi1iYjM4YTc3NDg2NGIiLCJlbWFpbF9pZCI6Im1lbWJlci1lbWFpbC1saXZlLWMxODcyZTIzLWRmMmItNDg0YS1hOWFhLTQ3MzNhMmM5MTNjYSIsInByb3ZpZGVyX3N1YmplY3QiOiIxMDAwMzkzNjgyMzI3MjQyMTEwNTQifX1dLCJyb2xlcyI6WyJzdHl0Y2hfbWVtYmVyIiwic3R5dGNoX2FkbWluIl19LCJpYXQiOjE3NjI0MjE2OTUsImlzcyI6Imh0dHBzOi8vYXBpLnN0eXRjaGIyYi5ncm9xLmNvbSIsIm5iZiI6MTc2MjQyMTY5NSwic3ViIjoibWVtYmVyLWxpdmUtMWNiMmM2ZTctMzAzYi00NjI5LWFhNmUtZmI2Zjg5MTFlMzcwIn0.INffalbKXlWHUAIT2g9tv1v0Nc2Tfugxe6-iP9fODGMoni5nCxd0dAbQfjYoFX3eIwwJiBnjc6u2TlkHe0OtbwCPjb3Y23OxERKaHY23yuPMCvY3cwuaegThRVmuvAbw1BqtRDAHmGzQVje07zNCdLQJzjJMa_y9gv6jRSQ7dHdU_M92HMTzuoosn6XVPCgTz02GWBWuZJZ645slUqkcRUp1-DHVapFMJ3lnWOXIQ7p-n1rGm8OdbnemxXKe81vA_IsOA9r7BhSy_oKLlYbsV8ru0F2IoQjpxYCbvpWIlv1bbx3OiKnlWRuMiN19ZkW90gT-MLVDY5ZZDUxU1lPyrA',
                'content-type': 'application/json',
                'groq-organization': 'org_01k92gvc0jf8ntz82tsctxyd12',
                'origin': 'https://console.groq.com',
                'priority': 'u=1, i',
                'referer': 'https://console.groq.com/',
                'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
                'x-stainless-arch': 'unknown',
                'x-stainless-lang': 'js',
                'x-stainless-os': 'Unknown',
                'x-stainless-package-version': '0.31.0',
                'x-stainless-retry-count': '0',
                'x-stainless-runtime': 'browser:chrome',
                'x-stainless-runtime-version': '141.0.0',
                'x-stainless-timeout': '60'
            }
            
            body = {
                "model": "openai/gpt-oss-120b",
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.3,
                "max_completion_tokens": 8192,
                "stream": False,
                "reasoning_effort": "high"
            }
            
            async with session.post(
                'https://api.groq.com/openai/v1/chat/completions?project_id=project_01k92gvcg6f8pveava7f06fw4g',
                headers=headers,
                json=body
            ) as resp:
                ai_data = await resp.json()
                
                # Проверяем статус ответа
                if resp.status != 200:
                    return web.json_response({'error': f'API error: {ai_data}'}, status=resp.status)
                
                content = ai_data.get('choices', [{}])[0].get('message', {}).get('content', 'No response from AI')
                
                return web.json_response({'response': content})
                
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

# Создаем веб-приложение
app = web.Application()
app.router.add_post('/groq', groq_handler)

async def start_web_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    print("Web server started on http://localhost:8080")

async def main():
    # Запускаем веб-сервер
    await start_web_server()
    # Запускаем телеграм-бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
