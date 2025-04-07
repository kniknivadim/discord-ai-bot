import discord
from discord.ext import commands
import openai
import asyncio

# ⚠️ Обязательно замени токены после тестов
DISCORD_TOKEN = ""
OPENAI_API_KEY = ""

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты помощник по управлению Discord сервером. Отвечай командами для управления Discord."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

@bot.event
async def on_ready():
    print(f'✅ Бот {bot.user} запущен!')

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

bot.run(DISCORD_TOKEN)
