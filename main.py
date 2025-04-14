import random

@dp.callback_query_handler(lambda c: c.data == "day_route")
async def day_route(callback_query: CallbackQuery):
    cards = [
        {
            "photo": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",  # дорога
            "caption": "🧭 Иногда ты продолжаешь идти, даже не чувствуя дороги.\nМетод «Маршрут» помогает остановиться и увидеть."
        },
        {
            "photo": "https://images.unsplash.com/photo-1497294815431-9365093b7331",  # человек у развилки
            "caption": "🚶‍♂️ Ты на развилке. Прямо — привычка. Вбок — ты сам.\nОстановись и выбери направление."
        },
        {
            "photo": "https://images.unsplash.com/photo-1530650052540-4693b1f4f33f",  # лес и солнце
            "caption": "🌞 Свет внутри есть. Просто тучи плотно легли. Снимем их по частям."
        },
        {
            "photo": "https://images.unsplash.com/photo-1488805990569-3c9e1d76d51c",  # городской шум
            "caption": "🔊 Вокруг — шум. Внутри — тишина. А ты где?"
        },
        {
            "photo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",  # камень в воде
            "caption": "🪨 Иногда покой — это не цель, а ловушка. Пора пошевелиться?"
        }
    ]
    selected = random.choice(cards)

    await callback_query.message.answer_photo(
        photo=selected["photo"],
        caption=selected["caption"]
    )
    await callback_query.message.answer("📊 Где ты ускоряешься, чтобы не чувствовать?")
    await callback_query.message.answer("📖 Что ты сегодня делаешь из привычки, а не из смысла?")
