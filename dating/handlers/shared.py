from aiogram.fsm.state import State, StatesGroup
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# MODELS SHARED AMONG HANDLERS

class UserForm(StatesGroup):
    # Account info
    username = State()
    user_id = State()
    # User info 
    age = State()
    gender = State()
    name = State()
    media = State()
    photo = State()
    # Bot states
    edit_profile = State()  # New state for editing profile, will add more fi
    completed = State()  # New state for completed profile

# Gender keyboard
gender_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Female")],
        [types.KeyboardButton(text="Male")],
        [types.KeyboardButton(text="Other")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Profile completion keyboard
profile_completion_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Edit Profile")],
        [types.KeyboardButton(text="Meet New People")],
        # [types.KeyboardButton(text="View Matches")]  # will add later
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Edit profile keyboard
edit_profile_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Edit Name")],
        [types.KeyboardButton(text="Edit Age")],
        [types.KeyboardButton(text="Edit Gender")],
        [types.KeyboardButton(text="Edit Media")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
