async def on_startup(dp):
    import facecontrolapp.bot.middlewares as middlewares
    import facecontrolapp.bot.filters as filters
    filters.setup(dp)
    middlewares.setup(dp)

    from .utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


def main():
    from aiogram import executor
    from facecontrolapp.bot.handlers import dp

    executor.start_polling(dp, on_startup=on_startup)


if __name__ == '__main__':
    main()
