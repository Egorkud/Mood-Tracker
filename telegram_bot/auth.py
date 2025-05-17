from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import aiohttp
from main import DJANGO_API_URL

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
                await msg.answer(f"Привіт, {data['username']}! Ви успішно увійшли.")
            else:
                await msg.answer("Користувача не знайдено. Спробуйте ще раз:")
