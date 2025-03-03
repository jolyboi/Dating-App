import asyncio 
import logging 
from aiogram import Bot, Dispatcher
from handlers.index import register_command_handlers
from handlers.edit import router as edit_router

# Bot token
BOT_TOKEN = ''

async def main():
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Register echo handlers
    register_command_handlers(dp)
    dp.include_router(edit_router)

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


# Entry point 
if __name__ == '__main__':
    asyncio.run(main())
