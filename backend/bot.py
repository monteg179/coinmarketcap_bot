import logging

from telegram import (
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    JobQueue,
)

from backend.coinmarketcap import (
    coin_market_cap_client,
)
from backend import settings

logger = logging.getLogger(__name__)


TELEGRAM_TOKEN = settings.enviroment.telegram_token
WEBHOOK_PORT = settings.enviroment.webhook_port
WEBHOOK_URL = settings.enviroment.webhook_url
WEBHOOK_SECRET = settings.enviroment.webhook_secret
WEBHOOK_PATH = settings.enviroment.webhook_path
WEBHOOK_CERT = settings.enviroment.webhook_cert
COIN_MARKET_CAP_INTERVAL = settings.COIN_MARKET_CAP_INTERVAL
JOB_INTERVAL = settings.JOB_INTERVAL


class BotJob:

    USAGE_MESSAGE = ('Usage: /add <coin> <low> <high>\n'
                     'coin: str\n'
                     'low: float\n'
                     'high: float')

    def __init__(self, user_id: int, args: list[str]) -> None:
        self.__user_id = user_id
        self.__coin = args[0].upper()
        self.__low = float(args[1])
        self.__high = float(args[2])
        self.__name = (f'{self.__user_id} - {self.__coin} - '
                       f'{self.__low} - {self.__high}')
        self.__title = f'{self.__coin.upper()}[{self.__low}, {self.__high}]'

    def __str__(self) -> str:
        return self.__title

    @property
    def name(self) -> str:
        return self.__name

    @property
    def title(self) -> str:
        return self.__title

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def coin(self) -> str:
        return self.__coin

    @property
    def low(self) -> float:
        return self.__low

    @property
    def high(self) -> float:
        return self.__high


def remove_job_from_queue(name: str, queue: JobQueue) -> str | None:
    jobs = queue.get_jobs_by_name(name)
    if jobs:
        for job in jobs:
            job.schedule_removal()
        return '\n'.join(
            [
                job.data.title
                for job in jobs
                if isinstance(job.data, BotJob)
            ]
        )


async def coin_market_cap_callback(
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await coin_market_cap_client.cryptocurrency()


async def jobs_callback(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job.data
    if isinstance(job, BotJob):
        price = coin_market_cap_client.prices.get(job.coin)
        if isinstance(price, float) and (price < job.low or price > job.high):
            await context.bot.send_message(
                chat_id=context.job.chat_id,
                text=f'{job.title}:\n{price:.4f}'
            )


async def add_command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    try:
        job = BotJob(user_id, context.args)
    except Exception:
        await context.bot.send_message(
            chat_id=chat_id,
            text=BotJob.USAGE_MESSAGE
        )
    else:
        remove_job = remove_job_from_queue(job.name, context.job_queue)
        context.job_queue.run_repeating(
            callback=jobs_callback,
            interval=JOB_INTERVAL,
            name=job.name,
            chat_id=chat_id,
            user_id=user_id,
            data=job
        )
        message = f'Add job:\n{job.title}'
        if remove_job:
            message = f'Remove job:\n{remove_job}\n\n{message}'
        await context.bot.send_message(
            chat_id=chat_id,
            text=message
        )


async def remove_command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    try:
        job = BotJob(user_id, context.args)
    except Exception:
        await context.bot.send_message(
            chat_id=chat_id,
            text=BotJob.USAGE_MESSAGE
        )
    else:
        remove_job = remove_job_from_queue(job.name, context.job_queue)
        message = 'Remove job:\n'
        if remove_job:
            message += job.title
        await context.bot.send_message(
            chat_id=chat_id,
            text=message
        )


async def list_command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    jobs = [
        job.data for job in context.job_queue.jobs()
        if (job.user_id == user_id and
            isinstance(job.data, BotJob))
    ]
    message = 'Jobs list:\n' + '\n'.join([job.title for job in jobs])
    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )


async def coins_command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    coins = [
        f'{key}: {value}'
        for key, value in coin_market_cap_client.coins.items()
    ]
    message = 'Coins list:\n' + '\n'.join(coins)
    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )


async def prices_command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    prices = [
        f'{key}: {value:.4f}'
        for key, value in coin_market_cap_client.prices.items()
    ]
    message = 'Prices list:\n' + '\n'.join(prices)
    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )


def run_bot() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.job_queue.run_repeating(
        callback=coin_market_cap_callback,
        interval=COIN_MARKET_CAP_INTERVAL,
        first=1.0
    )
    app.add_handler(
        CommandHandler('add', add_command_handler)
    )
    app.add_handler(
        CommandHandler('remove', remove_command_handler)
    )
    app.add_handler(
        CommandHandler('list', list_command_handler)
    )
    app.add_handler(
        CommandHandler('coins', coins_command_handler)
    )
    app.add_handler(
        CommandHandler('prices', prices_command_handler)
    )
    if all([WEBHOOK_PORT, WEBHOOK_URL, WEBHOOK_CERT]):
        app.run_webhook(
            listen='0.0.0.0',
            port=WEBHOOK_PORT,
            secret_token=WEBHOOK_SECRET,
            url_path=WEBHOOK_PATH,
            webhook_url=WEBHOOK_URL,
            cert=WEBHOOK_CERT,
            drop_pending_updates=True
        )
    else:
        app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
