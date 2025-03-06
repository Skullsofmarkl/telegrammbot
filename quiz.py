from database import get_quiz_index, update_quiz_index, update_score
from keyboards import generate_options_keyboard
from quiz_data import quiz_data

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(quiz_data[current_question_index]['question'], reply_markup=kb)

async def new_quiz(message):
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0)
    await update_score(user_id, reset=True)
    await get_question(message, user_id)