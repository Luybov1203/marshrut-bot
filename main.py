from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.executor import start_webhook
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import logging
import os
import random

# 🔐 ВСТАВЬ СЮДА ТОКЕН (если не используешь переменные окружения на Render)
API_TOKEN = "7638069426:AAFsxGjvX4uFokHPTufLqgXelr6nDlljsYQ"

# 🌐 Render сам подставит сюда свой URL, ничего менять не нужно
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 3000))

# Настройка логов и бота
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- Состояния (FSM) ---
class Form(StatesGroup):
    Q1 = State()
    Q2 = State()

# --- Клавиатуры ---
main_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("🔍 Узнать, где я сейчас", callback_data="diagnose"),
    InlineKeyboardButton("📅 Посмотреть метод", callback_data="method")
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
    InlineKeyboardButton("📍 Маршрут дня", callback_data="day_route"),
    InlineKeyboardButton("✉️ Записаться на мини-сессию", callback_data="session"),
    InlineKeyboardButton("👀 Узнать подробнее", callback_data="details"),
    InlineKeyboardButton("🔄 Пройти заново", callback_data="restart")
)

# --- Обработчики ---
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "🔍 <b>Здесь не будет мотивации.</b>\nЗато будет ясность.\n\nЕсли ты хочешь проверить, где ты сейчас — начнём.",
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
        "🧭 Ты перегружен. Не значит — сломан. Просто потерян фокус.\nМетод «Маршрут» начинается с точки. Вот твоя.",
        reply_markup=nav_kb
    )

@dp.callback_query_handler(lambda c: c.data == "method")
async def show_method(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "📅 Метод <b>«Маршрут»</b> — это инструмент ясности и навигации. Он помогает вернуться к себе.",
        reply_markup=nav_kb
    )

@dp.callback_query_handler(lambda c: c.data == "day_route")
async def day_route(callback_query: CallbackQuery):
    cards = [
        {
            "photo": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
            "caption": "🧭 Иногда ты продолжаешь идти, даже не чувствуя дороги.\nМетод «Маршрут» помогает остановиться и увидеть."
        },
        {
            "photo": "https://images.unsplash.com/photo-1497294815431-9365093b7331",
            "caption": "🚶‍♂️ Ты на развилке. Прямо — привычка. Слева — ты сам.\nОстановись и выбери направление."
        },
        {
            "photo": "https://images.unsplash.com/photo-1530650052540-4693b1f4f33f",
            "caption": "🌞 Свет внутри есть. Просто тучи плотно легли. Снимем их по частям."
        },
        {
            "photo": "https://images.unsplash.com/photo-1488805990569-3c9e1d76d51c",
            "caption": "🔊 Вокруг — шум. Внутри — тишина. А ты где?"
        },
        {
            "photo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
            "caption": "🪨 Иногда покой — это не цель, а ловушка. Пора пошевелиться?"
        }
    ]
    card = random.choice(cards)
    await callback_query.message.answer_photo(photo=card["photo"], caption=card["caption"])
    await callback_query.message.answer("📊 Где ты ускоряешься, чтобы не чувствовать?")
    await callback_query.message.answer("📖 Что ты сегодня делаешь из привычки, а не из смысла?")

@dp.callback_query_handler(lambda c: c.data == "session")
async def session(callback_query: CallbackQuery):
    await callback_query.message.answer("😊 Иногда достаточно 15 минут, чтобы повернуть в сторону себя.\nХочешь посмотреть на свою точку? Напиши мне в ответ или запишись.")

@dp.callback_query_handler(lambda c: c.data == "details")
async def details(callback_query: CallbackQuery):
    await callback_query.message.answer("Метод поможет тебе услышать себя, соблюсти баланс между личными отношениями и работой, в приоритетах. Это про смысл, а не про мотивацию.")

@dp.callback_query_handler(lambda c: c.data == "restart")
async def restart(callback_query: CallbackQuery):
    await cmd_start(callback_query.message)

# --- Webhook setup ---
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown(dp):
    logging.warning("Webhook удалён")
    await bot.delete_webhook()

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
