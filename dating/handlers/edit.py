from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from .shared import UserForm, profile_completion_keyboard, gender_keyboard
import logging

router = Router()


async def return_to_edit_menu(message: types.Message, state: FSMContext):
    logging.info('Returning to completion menu') # show them logs

    data = await state.get_data()
    media_file_id = data.get('media_file_id')

    await message.answer("Your profile has been updated! 🎉")
    confirmation_message = (
        "Here's your complete profile:\n\n"
        f"👤 Name: {data.get('name')}\n"
        f"🎂 Age: {data.get('age')}\n"
        f"🚻 Gender: {data.get('gender')}"
    )

    await message.answer(confirmation_message, reply_markup=profile_completion_keyboard)
    await message.answer_video_note(media_file_id)
    await state.set_state(UserForm.completed)



@router.message(F.text == "Edit Name", UserForm.edit_profile)
async def edit_name_handler(message: types.Message, state: FSMContext):
    await message.answer("Please enter your new name.", reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(edit=True)
    await state.set_state(UserForm.name)

    
@router.message(F.text == "Edit Age", UserForm.edit_profile)
async def edit_age_handler(message: types.Message, state: FSMContext):
    await message.answer("Please enter your new age.", reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(edit=True)
    await state.set_state(UserForm.age)


@router.message(F.text == "Edit Gender", UserForm.edit_profile)
async def edit_gender_handler(message: types.Message, state: FSMContext):
    await message.answer("Please select your new gender.", reply_markup=gender_keyboard)
    await state.update_data(edit=True)
    await state.set_state(UserForm.gender)


@router.message(F.text == "Edit Media", UserForm.edit_profile)
async def edit_media_handler(message: types.Message, state: FSMContext):
    await message.answer("Please send a new voice message or circle video.", reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(edit=True)
    await state.set_state(UserForm.media)
