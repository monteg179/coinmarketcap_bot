import logging

from telegram import (
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from backend import settings

logger = logging.getLogger(__name__)


TELEGRAM_TOKEN = settings.enviroment.telegram_token
WEBHOOK_PORT = settings.enviroment.webhook_port
WEBHOOK_URL = settings.enviroment.webhook_url
WEBHOOK_SECRET = settings.enviroment.webhook_secret
WEBHOOK_PATH = settings.enviroment.webhook_path
WEBHOOK_CERT = settings.enviroment.webhook_cert


async def start_command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    name = update.effective_user.name
    full_name = update.effective_user.full_name
    await context.bot.send_message(
        chat_id=chat_id,
        text=f'id = {user_id}\nname = {name}\nfull name = {full_name}'
    )


def build_bot_application() -> Application:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(
        CommandHandler('start', start_command_handler)
    )
    return app


def run_bot_application(app: Application) -> None:
    if all([WEBHOOK_PORT, WEBHOOK_URL, WEBHOOK_CERT]):
        app.run_webhook(
            listen='0.0.0.0',
            port=WEBHOOK_PORT,
            secret_token=WEBHOOK_SECRET,
            url_path=WEBHOOK_PATH,
            webhook_url=WEBHOOK_URL,
            cert=WEBHOOK_CERT,
        )
    else:
        app.run_polling(allowed_updates=Update.ALL_TYPES)
