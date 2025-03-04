from aiogram import Router, types
import json
import os

router = Router()
GREETING_FILE = "data/greetings.json"

def load_greeting():
    if os.path.exists(GREETING_FILE):
        with open(GREETING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_greeting(chat_id, message):
    greetings = load_greeting()
    greetings[str(chat_id)] = message
    with open(GREETING_FILE, "w", encoding="utf-8") as f:
        json.dump(greetings, f, ensure_ascii=False)

@router.message(commands=["set_welcome"])
async def set_welcome(msg: types.Message):
    if msg.chat.type != "private":
        text = msg.text.split(maxsplit=1)
        if len(text) < 2:
            await msg.reply("Отправьте команду в формате: /set_welcome [текст]. Используйте `{user}` для упоминания.", parse_mode="Markdown")
            return
        save_greeting(msg.chat.id, text[1])
        await msg.reply("Приветствие обновлено!")

@router.message()
async def welcome_new_members(msg: types.Message):
    if msg.new_chat_members:
        greetings = load_greeting()
        greeting = greetings.get(str(msg.chat.id), "Добро пожаловать, {user}!")
        for user in msg.new_chat_members:
            mention = f"[{user.full_name}](tg://user?id={user.id})"
            await msg.answer(greeting.replace("{user}", mention), parse_mode="Markdown")
