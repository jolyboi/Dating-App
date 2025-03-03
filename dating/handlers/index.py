from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
import logging
from handlers.edit import return_to_edit_menu
from .shared import UserForm, edit_profile_keyboard, profile_completion_keyboard, gender_keyboard

router = Router()


@router.message(Command('start'))
async def start_command_handler(message: types.Message, state: FSMContext):
    # Get user id and username and save to state
    user_id = message.from_user.id
    username = message.from_user.username

    await state.update_data(user_id=user_id)
    await state.update_data(username=username)

    # Output hello message
    hello_message = f"Welcome to NeuroLove, {username} 😍\n\nI'll help you find a partner or just friends 👫"
    await message.answer(hello_message)

    # Prompt for age 
    await asyncio.sleep(1)  # Sleep for 1 second
    await message.answer('What is your age?')
    await state.set_state(UserForm.age)



# Age prompt handler 
@router.message(UserForm.age)
async def age_handler(message: types.Message, state: FSMContext):
     # Check if editing, true if editing
    data = await state.get_data()
    edit = data.get('edit')
    # Check if message is a number (age)
    if message.text.isdigit():
        age = int(message.text)
        if age < 18:
            await message.answer("You're too young!")
            await state.clear()
        else:
            await state.update_data(age=age)
            await asyncio.sleep(1) # Sleep for 1 seconds
            # Checking if editing, if so return to edit menu
            if edit:
                await return_to_edit_menu(message, state)
            else:
                await message.answer('Great! Now tell me your gender?', reply_markup=gender_keyboard)
                await state.set_state(UserForm.gender)
    else:
        await message.answer("Please enter a valid age (numbers only).")



# Gender prompt handler 
@router.message(UserForm.gender)
async def gender_handler(message: types.Message, state: FSMContext):
    # Check if editing, true if editing
    data = await state.get_data()
    edit = data.get('edit')
    # Check if the input is valid
    if message.text in ["Female", "Male", "Other"]:
        # Save gender and move to next state
        await state.update_data(gender=message.text)
        await asyncio.sleep(1) # Sleep for 1 seconds
        # Checking if editing, if so return to edit menu
        if edit:
            await return_to_edit_menu(message, state)
        else:
            await message.answer(f"Got it! Finally, what is your name?", reply_markup=types.ReplyKeyboardRemove())  
            await state.set_state(UserForm.name)
    else:
        # Show the keyboard again if input is invalid
        await message.answer("Please select your gender:", reply_markup=gender_keyboard)



# Name prompt handler
@router.message(UserForm.name)
async def name_handler(message: types.Message, state: FSMContext):
    # Check if editing, true if editing
    data = await state.get_data()
    edit = data.get('edit')
    # Get the name from the message
    name = message.text.strip()
    
    # Basic validation
    if len(name) < 2:
        await message.answer("Please enter a valid name (at least 1 characters)")
        return 
    
    # Save the name and complete the form
    await state.update_data(name=name)
    await asyncio.sleep(1)  # Sleep for 1 second
    
    if edit:
        await state.update_data(edit=False)
        await return_to_edit_menu(message, state)

    else:   
        # Prompt for media
        await message.answer(
            f"Thank you, {name}! Now let's record a voice message or a circle video of yourself."
        )
        await state.set_state(UserForm.media)



@router.message(UserForm.media)
async def media_handler(message: types.Message, state: FSMContext):
    # Check if editing, true if editing
    data = await state.get_data()
    edit = data.get('edit')
    
    # Check if message is a voice message or a circle video
    if message.voice:
        # Handle voice message
        await state.update_data(voice_file_id=message.voice.file_id)
        await message.answer("Great! Now please send me a photo to create your profile video.")
        await state.set_state(UserForm.photo)  # Transition to photo state
        return
    elif message.video_note:
        # Handle circle video
        await state.update_data(media_type="video_note", media_file_id=message.video_note.file_id)
        # Checking if editing, if so return to edit menu
        if edit:
            await return_to_edit_menu(message, state)
        else:
            await show_completion(message, state, "video_note", message.video_note.file_id)
            return
    else:
        await message.answer("Please send either a voice message or a circle video.")


async def show_completion(message: types.Message, state: FSMContext, file_type: str, file_id: str):
    # Get all collected data
    data = await state.get_data()
    
    confirmation_message = (
        "Thank you! Here's your complete profile:\n\n"
        f"👤 Name: {data.get('name')}\n"
        f"🎂 Age: {data.get('age')}\n"
        f"🚻 Gender: {data.get('gender')}"
    )
    
    # Send confirmation message
    await message.answer(confirmation_message)
    
    # Send the media file
    await message.answer_video_note(file_id) 

    # Show the profile completion message
    logging.info("Showing profile completion...")
    await message.answer("Your profile is now complete! 🎉")
    
    # Transition to the completed state
    await state.set_state(UserForm.completed)
    
    # Explicitly call the completed handler to ensure it's triggered
    await completed_handler(message, state)


@router.message(F.text == "Edit Profile", UserForm.completed,)
async def edit_profile_handler(message: types.Message, state: FSMContext):
    logging.info("Edit profile handler triggered!")
    await asyncio.sleep(1)  # Sleep for 1 second
    await message.answer("What would you like to edit?", reply_markup=edit_profile_keyboard)
    await state.set_state(UserForm.edit_profile)



@router.message(F.text == "Meet New People", UserForm.completed)
async def meet_new_people_handler(message: types.Message, state: FSMContext):
    await message.answer("Let's find someone new for you!")
    # Here you can add logic for meeting new people
    # await state.clear()
    await start_command_handler(message, state)  # Restart the process



@router.message(UserForm.completed)
async def completed_handler(message: types.Message, state: FSMContext):
    # Show the profile completion keyboard
    logging.info("Showing profile completion keyboard")  # show them logs
    await asyncio.sleep(1)  # Sleep for 1 second
    await message.answer("What would you like to do next?", reply_markup=profile_completion_keyboard)
    await state.set_state(UserForm.completed)




def register_command_handlers(dp):
    dp.include_router(router)



    

       
