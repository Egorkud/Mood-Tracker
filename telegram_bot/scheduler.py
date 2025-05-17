from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot_instance import bot

# Тут ми зберігаємо ID користувача і його токен
logged_users = {}


# Додаємо користувача до списку для нагадування
async def add_logged_user(user_id: int, token: str):
    logged_users[user_id] = token


# Щоденне завдання: надсилаємо нагадування кожному
async def send_daily_reminders():
    for user_id in logged_users.keys():
        try:
            await bot.send_message(user_id, "📋 Не забудьте зробити новий запис про свій настрій!")
        except Exception as e:
            print(f"Помилка при надсиланні до {user_id}: {e}")


# Запуск планувальника
def start_scheduler():
    scheduler = AsyncIOScheduler()

    # Тестовий режим (можна закоментувати)
    scheduler.add_job(send_daily_reminders, "interval", minutes=1)
    # Щодня о 20:00 за серверним часом
    scheduler.add_job(send_daily_reminders, "cron", hour=20, minute=00)
    scheduler.start()
