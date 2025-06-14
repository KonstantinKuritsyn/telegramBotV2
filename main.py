from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, PicklePersistence
import random
import datetime
import pytz
import os

moscow_tz = pytz.timezone('Europe/Moscow')

wishes = [
    "Пусть этот день принесёт тебе радость и удачу!",
    "Желаю отличного настроения и вдохновения на весь день!",
    "Пусть сегодня всё получится так, как ты задумал!",
    "Улыбайся чаще — это украшает твой день!",
    "Желаю крепкого здоровья и много приятных моментов!",
    "Пусть сегодня будет повод для гордости собой!",
    "Желаю встретить только добрых и искренних людей!",
    "Пусть каждый час этого дня будет наполнен счастьем!",
    "Пусть удача сопутствует тебе во всех делах!",
    "Желаю гармонии, тепла и уюта в душе!",
    "Пусть этот день будет светлым и радостным!",
    "Желаю найти время для себя и своих увлечений!",
    "Пусть сегодня сбудется хотя бы одно твое желание!",
    "Желаю вдохновения и творческих успехов!",
    "Пусть этот день принесёт только хорошие новости!",
    "Желаю уверенности в своих силах и побед!",
    "Пусть рядом будут только верные друзья!",
    "Желаю мира и спокойствия в душе!",
    "Пусть сегодня будет повод для улыбки!",
    "Желаю тебе настоящего счастья сегодня и всегда!",
    "Пусть этот день принесёт тебе только радость и улыбки!",
    "Желаю тебе лёгкости во всех начинаниях!",
    "Пусть сегодня всё складывается наилучшим образом!",
    "Желаю, чтобы каждый момент был наполнен счастьем!",
    "Пусть удача сопровождает тебя на каждом шагу!",
    "Желаю вдохновения и творческих успехов!",
    "Пусть рядом будут только добрые и искренние люди!",
    "Желаю гармонии в душе и покоя в сердце!",
    "Пусть сегодня сбудется хотя бы одна твоя мечта!",
    "Желаю уверенности в своих силах и веры в себя!",
    "Пусть день будет наполнен приятными сюрпризами!",
    "Желаю крепкого здоровья и бодрого настроения!",
    "Пусть каждый час этого дня будет особенным!",
    "Желаю найти повод для радости даже в мелочах!",
    "Пусть сегодня будет много приятных встреч и событий!",
    "Желаю тебе внутренней гармонии и тепла!",
    "Пусть всё задуманное обязательно исполнится!",
    "Желаю, чтобы день прошёл легко и продуктивно!",
    "Пусть твоя улыбка озаряет этот день!",
    "Желаю море позитива и хорошего настроения!",
    "Пусть сегодня будет день новых возможностей!",
    "Желаю тебе спокойствия и уверенности в будущем!",
    "Пусть этот день подарит вдохновение для новых свершений!",
    "Желаю приятных открытий и радостных новостей!",
    "Пусть каждый миг будет наполнен любовью и заботой!",
    "Желаю тебе гармонии с собой и окружающим миром!",
    "Пусть сегодня будет больше поводов для счастья!",
    "Желаю, чтобы день прошёл легко и без забот!",
    "Пусть удача будет твоим постоянным спутником!",
    "Желаю, чтобы каждый твой шаг вёл к успеху!"
]

flowers = [
    "🌸",  # Цветок сакуры
    "🌷",  # Тюльпан
    "🌹",  # Роза
    "🌺",  # Гибискус
    "🌻",  # Подсолнух
    "🌼",  # Ромашка
    "🌿",  # Ветка
    "🍀",  # Клевер
    "🍁",  # Кленовый лист
    "🍂",  # Осенний лист
    "🍃",  # Лист
    "🍄",  # Гриб
    "💐",  # Букет
]


async def send_daily_color(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    wish = random.choice(wishes)
    flower = random.choice(flowers)
    await context.bot.send_message(chat_id=chat_id, text=f"{wish} {flower}")


async def start(update, context):
    chat_id = update.effective_chat.id
    await update.message.reply_text("Привет! Я буду каждый день писать тебе приятные пожелания")
    # Сохраняем chat_id в chat_data
    context.application.chat_data[chat_id]['subscribed'] = True
    # Удаляем старую задачу, если есть
    remove_job_if_exists(str(chat_id), context)
    # Запускаем новую ежедневную задачу
    time_to_send = datetime.time(hour=19, minute=20, tzinfo=moscow_tz)
    context.job_queue.run_daily(send_daily_color, time=time_to_send, chat_id=chat_id, name=str(chat_id))
    await update.message.reply_text("Начинаю отправлять пожелания")


async def restore_jobs(app):
    for chat_id, data in app.chat_data.items():
        if data.get('subscribed'):
            time_to_send = datetime.time(hour=19, minute=20, tzinfo=moscow_tz)
            app.job_queue.run_daily(
                send_daily_color,
                time=time_to_send,
                chat_id=chat_id,
                name=str(chat_id)
            )


def remove_job_if_exists(name: str, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def stop(update, context):
    chat_id = update.effective_chat.id
    removed = remove_job_if_exists(str(chat_id), context)
    context.chat_data['subscribed'] = False
    if removed:
        await update.message.reply_text("Автоматическая отправка остановлена.")
    else:
        await update.message.reply_text("У вас не было активных задач.")


if __name__ == '__main__':
    persistence = PicklePersistence(filepath='bot_data')
    app = ApplicationBuilder().token(os.environ.get('TELEGRAM_TOKEN')).persistence(persistence).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    print("Бот запущен...")

    # Восстановление задач
    app.post_init = restore_jobs

    app.run_polling()
