# coinmarketcap_bot

## ОПИСАНИЕ
Бот обрабатывает команды: `add`, `remove`, `list`
- `add`: добавляет задание в планировщик
- `remove`: удаляет задание из планировщика
- `list`: просмотр заданий планировщика


## ЗАПУСК
1. клонировать репозиторий:
```sh
git clone https://github.com/monteg179/coinmarketcap_bot.git
cd coinmarketcap_bot
```
2. создать файл `.env` с таким содержанием
```
TELEGRAM_TOKEN=<token>
```
3. создать виртуальное окружение и запустить бота
```sh
poetry install
poetry shell
poetry run bot
```

## ИСПОЛЬЗОВАНИЕ
- добавить задание: `/add <coin> <low> <high>`<br>например: `/add BTC 0.0 10.0`
- удалить задание: `/remove <coin> <low> <high>`<br>например: `/remove BTC 0.0 10.0`
- задания планировщика: `/list`

## ТЕХНОЛОГИИ
- Python 3.11
- Poetry
- Python-Telegram-Bot
- Docker
- Github Actions

## АВТОРЫ
* Сергей Кузнецов - monteg179@yandex.ru
