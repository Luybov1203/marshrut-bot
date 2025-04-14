from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging
import os
import random

# 🔐 Прямой токен (если не используешь os.getenv)
API_TOKEN = "7638069426:AAFsxGjvX4uFokHPTufLqgXelr6nDlljsYQ"

# 🌐 Настройки вебхука для Render
WEBHOOK_HOST = "https://marshrut-bot.onrender.com"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 3000))

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- Состояния ---
class Form(StatesGroup):
    Q1 = State()
    Q2 = State()

# --- Клавиатуры ---
main_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("\ud83d\udd0d Узнать, где я сейчас", callback_data="diagnose"),
    InlineKeyboardButton("\ud83d\uddd5 Посмотреть метод", callback_data="method")
)

diag_q1 = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Работа", callback_data="q1_Работа"),
    InlineKeyboardButton("Семья", callback_data="q1_Семья"),
    InlineKeyboardButton("Я сам(а)", callback_data="q1_Я сам(а)"),
    InlineKeyboardButton("Всё сразу", callback_data="q1_Всё сразу"),
    InlineKeyboardButton("Не знаю", callback_data="q1_Не знаю")
)

diag_q2 = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Ответственность, от которой устал", callback_data="q2_ответственность"),
    InlineKeyboardButton("Нет контроля, всё рушится", callback_data="q2_контроль"),
    InlineKeyboardButton("Хочу изменений, но боюсь", callback_data="q2_боюсь"),
    InlineKeyboardButton("Просто пустота", callback_data="q2_пустота")
)

nav_kb = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("\ud83d\udccd Маршрут дня", callback_data="day_route"),
    InlineKeyboardButton("\u2709\ufe0f Записаться на мини-сессию", callback_data="session"),
    InlineKeyboardButton("\ud83d\udc40 Узнать подробнее", callback_data="details"),
    InlineKeyboardButton("\ud83d\udd04 Пройти заново", callback_data="restart")
)

# --- Обработчики ---
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "\ud83d\udd0d <b>Здесь не будет мотивации.</b>\nЗато будет ясность.\n\nЕсли ты хочешь проверить, где ты сейчас — начнём.",
        reply_markup=main_menu
    )

@dp.callback_query_handler(lambda c: c.data == "diagnose")
async def handle_diagnose(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Что сейчас требует твоего внимания больше всего?", reply_markup=diag_q1)
    await Form.Q1.set()

@dp.callback_query_handler(lambda c: c.data.startswith("q1_"), state=Form.Q1)
async def handle_q1(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(q1=callback_query.data[3:])
    await callback_query.message.edit_text("Что ты чувствуешь в этой сфере?", reply_markup=diag_q2)
    await Form.Q2.set()

@dp.callback_query_handler(lambda c: c.data.startswith("q2_"), state=Form.Q2)
async def handle_q2(callback_query: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.edit_text(
        "\ud83e\udde1 Ты перегружен. Не значит — сломан. Просто потерян фокус.\nМетод «Маршрут» начинается с точки. Вот твоя.",
        reply_markup=nav_kb
    )

@dp.callback_query_handler(lambda c: c.data == "method")
async def show_method(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "\ud83d\uddd5 Метод <b>«Маршрут»</b> — это инструмент ясности и навигации. Он помогает вернуться к себе.",
        reply_markup=nav_kb
    )

@dp.callback_query_handler(lambda c: c.data == "day_route")
async def day_route(callback_query: CallbackQuery):
    cards = [
        {"photo": "https://images.unsplash.com/photo-1506744038136-46273834b3fb", "caption": "\ud83d\uddd0 Иногда ты продолжаешь идти, даже не чувствуя дороги."},
        {"photo": "https://images.unsplash.com/photo-1497294815431-9365093b7331", "caption": "\ud83d\udeb6\u200d♂️ Прямо — привычка. Слева — ты сам. Остановись и выбери направление."},
        {"photo": "https://images.unsplash.com/photo-1530650052540-4693b1f4f33f", "caption": "\ud83c\udf1e Свет внутри есть. Просто тучи легли. Снимем их по частям."},
        {"photo": "https://images.unsplash.com/photo-1488805990569-3c9e1d76d51c", "caption": "\ud83d\udd0a Вокруг — шум. Внутри — тишина. А ты где?"},
        {"photo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", "caption": "\ud83e\udea8 Иногда покой — ловушка. Пора пошевелиться?"},
    ]
    card = random.choice(cards)
    await callback_query.message.answer_photo(photo=card["photo"], caption=card["caption"])
    await callback_query.message.answer("\ud83d\udcca Где ты ускоряешься, чтобы не чувствовать?")
    await callback_query.message.answer("\ud83d\udcd6 Что ты сегодня делаешь из привычки, а не из смысла?")

@dp.callback_query_handler(lambda c: c.data == "session")
async def session(callback_query: CallbackQuery):
    await callback_query.message.answer("\ud83d\ude0a Иногда достаточно 15 минут, чтобы повернуть в сторону себя.\nХочешь посмотреть на свою точку? Напиши мне в ответ или запишись.")

@dp.callback_query_handler(lambda c: c.data == "details")
async def details(callback_query: CallbackQuery):
    await callback_query.message.answer("Метод помогает услышать себя, соблюсти баланс между отношениями и работой. Это про смысл, а не мотивацию.")

@dp.callback_query_handler(lambda c: c.data == "restart")
async def restart(callback_query: CallbackQuery):
    await cmd_start(callback_query.message)

# --- Webhook ---
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown(dp):
    await bot.delete_webhook()
    logging.warning("Webhook удалён")

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
