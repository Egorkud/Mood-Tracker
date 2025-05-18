import aiohttp
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from main import DJANGO_API_URL
from scheduler import add_logged_user

router = Router()


class AuthState(StatesGroup):
    waiting_for_email = State()


@router.message(F.text == "/start")
async def start_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Привіт! Введи свою email адресу для входу:")
    await state.set_state(AuthState.waiting_for_email)


@router.message(AuthState.waiting_for_email)
async def process_email(msg: types.Message, state: FSMContext):
    email = msg.text.strip()
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{DJANGO_API_URL}/api/telegram/login/", json={"email": email}) as resp:
            if resp.status == 200:
                data = await resp.json()
                await state.clear()
                await state.update_data(token=data['access'])

                keyboard = ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="📊 Отримати статистику за тиждень")],
                    ],
                    resize_keyboard=True
                )
                await msg.answer(
                    f"Привіт, {data['username']}! Ви успішно увійшли.",
                    reply_markup=keyboard
                )
                await state.clear()
                await add_logged_user(msg.from_user.id, data['access'])
            else:
                await msg.answer("Користувача не знайдено. Спробуйте ще раз:")


@router.message(AuthState.waiting_for_email)
@router.message(F.text == "📊 Отримати статистику за тиждень")
async def weekly_stats_handler(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    from scheduler import logged_users  # ⬅ імпортуємо список залогінених

    if user_id not in logged_users:
        await msg.answer("Ви не увійшли в систему. Спочатку використайте /start.")
        return

    token = logged_users[user_id]

    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {token}"}
        async with session.get(f"{DJANGO_API_URL}/api/mood/stats/weekly/", headers=headers) as resp:
            if resp.status == 200:
                stats = await resp.json()
                message = (
                    "<b>Статистика за останній тиждень:</b>\n"
                    f"Кількість записів: {stats['entries_count']}\n"
                    f"Середній настрій: {stats['average_mood']:.1f} / 5 {stats['emotion_image']}\n"
                    f"Найчастіша емоція: {stats['most_common_emotion']}"
                )
                await msg.answer(message, parse_mode="HTML")
            else:
                await msg.answer("Не вдалося отримати статистику. Спробуйте пізніше, або додайте дані.")
