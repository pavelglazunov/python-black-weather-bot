import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from config.config import load_config
from src.handlers import routers
from src.middlewares import APIMiddleware, MessageInPrivateMiddleware, GetConfigMiddleware

logger = logging.getLogger(__name__)


async def main():
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Start bot")

    config = load_config()
    bot: Bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode='HTML'),
    )

    dp: Dispatcher = Dispatcher()

    dp.include_routers(*routers)

    dp.message.outer_middleware(MessageInPrivateMiddleware())
    dp.message.outer_middleware(GetConfigMiddleware(config))
    dp.message.outer_middleware(APIMiddleware(config))

    dp.callback_query.outer_middleware(GetConfigMiddleware(config))
    dp.callback_query.outer_middleware(APIMiddleware(config))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
