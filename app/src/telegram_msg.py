"""
    Description:

    Avisos pelo Telegram

    Author:           @Palin
    Created:          2021-05-25
    Copyright:        (c) Ampere Consultoria Ltda
"""
try:
    from dynaconf import Dynaconf

    settings = Dynaconf(
        envvar_prefix="AMPERE",
        settings_files=["settings.toml", ".secrets.toml"],
        environments=True,
        load_dotenv=True,
    )

    import telegram
    from telegram import ParseMode
except ImportError as error:
    print(error)
    print(f"error.name: {error.name}")
    print(f"error.path: {error.path}")


def notify_telegram(message):
    bot = telegram.Bot(token=settings.telegram_token)
    bot.sendMessage(
        chat_id=settings.telegram_chat_id, parse_mode=ParseMode.MARKDOWN, text=message
    )
