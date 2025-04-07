import discord
from discord.ext import commands
import openai
import asyncio
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение токенов из переменных окружения
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка наличия токенов
if not DISCORD_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Токены DISCORD_TOKEN или OPENAI_API_KEY не найдены в переменных окружения!")

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Настройка бота
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Функция для запроса к GPT
async def ask_gpt(prompt):
    try:
        response = await asyncio.to_thread(
            openai.chat.completions.create,
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты помощник по управлению Discord сервером. Отвечай командами для управления Discord."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка при запросе к GPT: {e}"

# Событие: бот готов
@bot.event
async def on_ready():
    print(f'✅ Бот {bot.user} запущен!')

# Событие: обработка сообщений
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    user_input = message.content
    await message.channel.typing()
    
    gpt_reply = await ask_gpt(user_input)

    await message.channel.send(f"💡 GPT предлагает:\n```{gpt_reply}```")

    # Пример выполнения простого запроса на создание канала
    if "создай канал" in gpt_reply.lower():
        try:
            channel_name = gpt_reply.lower().split("канал")[1].strip().strip('"')
            guild = message.guild
            await guild.create_text_channel(channel_name)
            await message.channel.send(f"✅ Канал `{channel_name}` создан!")
        except Exception as e:
            await message.channel.send(f"❌ Ошибка при создании канала: {e}")

# Запуск бота с обработкой ошибок
async def main():
    try:
        await bot.start(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("❌ Ошибка входа: неверный токен Discord!")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())
