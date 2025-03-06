from aiogram import Router, types, F
from aiogram.filters.command import Command
from quiz import  get_question, new_quiz
from keyboards import start_keyboard
from database import get_quiz_index, get_score, update_quiz_index, update_score
from quiz_data import quiz_data


router = Router()

async def handle_answer(callback: types.CallbackQuery, is_correct: bool, user_id: int):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(user_id)
    correct_option = quiz_data[current_question_index]['correct_option']

    if is_correct:
        await callback.message.answer("Верно!")
        await update_score(user_id, increment=True)  # Увеличиваем счетчик правильных ответов
    else:
        await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        score = await get_score(user_id)
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен! Вы дали {score} правильных ответов.")

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в квиз!", reply_markup=start_keyboard())

@router.message(F.text == "Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)
    
@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=True, user_id=callback.from_user.id)

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=False, user_id=callback.from_user.id)