from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import logging
import os

API_TOKEN = os.getenv("BOT_TOKEN") or "PASTE_YOUR_TOKEN_HERE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- Клавиатуры ---
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add("🔍 Узнать, где я сейчас", "📅 Посмотреть метод")

nav_kb = ReplyKeyboardMarkup(resize_keyboard=True)
nav_kb.add("🔄 Пройти заново", "📍 Маршрут дня")
nav_kb.add("✉️ Записаться на мини-сессию", "👀 Узнать подробнее")
nav_kb.add("⬅️ Вернуться в начало")

q1_kb = ReplyKeyboardMarkup(resize_keyboard=True)
q1_kb.add("Работа", "Семья", "Я сам(а)")
q1_kb.add("Всё сразу", "Не знаю")

q2_kb = ReplyKeyboardMarkup(resize_keyboard=True)
q2_kb.add("Ответственность, от которой устал")
q2_kb.add("Нет контроля, всё рушится")
q2_kb.add("Хочу изменений, но боюсь трогать")
q2_kb.add("Просто пустота")

# --- Состояния ---
class Form(StatesGroup):
    Q1 = State()
    Q2 = State()

# --- Обработчики ---
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    text = "🔍 Здесь не будет мотивации.\nЗато будет ясность.\n\nЕсли ты хочешь проверить, где ты сейчас — начнём."
    await message.answer(text, reply_markup=main_kb)

@dp.message_handler(lambda m: m.text == "🔍 Узнать, где я сейчас")
async def start_diag(message: types.Message):
    await message.answer("Что сейчас требует твоего внимания больше всего?", reply_markup=q1_kb)
    await Form.Q1.set()

@dp.message_handler(state=Form.Q1)
async def q1_answer(message: types.Message, state: FSMContext):
    await state.update_data(q1=message.text)
    await message.answer("Что ты чувствуешь в этой сфере?", reply_markup=q2_kb)
    await Form.Q2.set()

@dp.message_handler(state=Form.Q2)
async def q2_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q1 = data.get("q1")
    q2 = message.text

    response = "Ты перегружен. Не значит — сломан. Просто потерян фокус.\nМетод «Маршрут» начинается с точки. Вот твоя."
    await message.answer(response)
    await message.answer("📍 Хочу увидеть свой маршрут", reply_markup=nav_kb)
    await state.finish()

@dp.message_handler(lambda m: m.text == "📅 Посмотреть метод")
async def show_method(message: types.Message):
    await message.answer("Метод 'Маршрут' — это инструмент ясности и навигации. Он помогает вернуться к себе.", reply_markup=nav_kb)

@dp.message_handler(lambda m: m.text == "📍 Маршрут дня")
async def route_of_day(message: types.Message):
    questions = [
        "📊 Где ты ускоряешься, чтобы не чувствовать?",
        "📖 Что ты сегодня делаешь из привычки, а не из смысла?"
    ]
    for q in questions:
        await message.answer(q)

@dp.message_handler(lambda m: m.text == "✉️ Записаться на мини-сессию")
async def book_meeting(message: types.Message):
    await message.answer("😊 Иногда достаточно 15 минут, чтобы повернуть в сторону себя. Напиши, если хочешь договориться о встрече.")

@dp.message_handler(lambda m: m.text == "👀 Узнать подробнее")
async def more_info(message: types.Message):
    await message.answer("Метод помогает предпринимателям и их семьям навести порядок в приоритетах. Это про смысл, а не про мотивацию.")

@dp.message_handler(lambda m: m.text in ["🔄 Пройти заново", "⬅️ Вернуться в начало"])
async def restart(message: types.Message):
    await send_welcome(message)

# --- Запуск ---
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
