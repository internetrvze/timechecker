from asyncio import run as _runner, gather as _gather, sleep
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from functools import lru_cache
from dotenv import load_dotenv
from aiosqlite import connect
from logger import Logger
from time import time
from os import getenv


@lru_cache()
async def loadVariables() -> None:
    global bot, bot_id, db, logger, checker_id
    load_dotenv()
    bot = AsyncTeleBot(getenv('BOT_TOKEN'))
    bot_id = int(getenv('BOT_TOKEN').split(':')[0])
    logger = Logger()
    db = getenv('DATABASE_PATH')
    checker_id = getenv('CHECKER_UB_ID')
    async with connect(db) as _DB:
        await _DB.execute(
            'CREATE TABLE IF NOT EXISTS users ('
            'id INTEGER, '
            'full_name BLOB, '
            'chat_id INTEGER, '
            'last_message_time INTEGER, '
            'last_message_text BLOB, '
            'last_message_id INTEGER'
            ')'
        )
        await _DB.commit()


_runner(loadVariables())


class DB():
    @lru_cache()
    def __init__(self) -> None:
        pass

    async def checkDBexists(self, id: int, chat_id: int) -> bool:
        async with connect(db) as _DB:
            if len(
                await _DB.execute_fetchall(
                    'SELECT id FROM users '
                    f'WHERE chat_id={chat_id} AND id={id}'
                )
            ):
                return True
        return False

    async def databaseAdd(self, message: Message) -> None:
        message_text = message.caption if message.caption else message.text
        async with connect(db) as _DB:
            try:
                if await self.checkDBexists(message.from_user.id, message.chat.id):
                    await _DB.execute(
                        'UPDATE users SET '
                        f'last_message_time = {int(time())}, '
                        f'last_message_id = {message.id}, '
                        f'last_message_text = "{message_text.encode().hex()}"'
                        f' WHERE id = {message.from_user.id} '
                        f'AND chat_id = {message.chat.id}'
                    )
                    return await _DB.commit()

                await _DB.execute(
                    'INSERT INTO users ('
                    'id, full_name, chat_id, last_message_time, '
                    'last_message_text, last_message_id'
                    f') values ({message.from_user.id}, '
                    f'"{message.from_user.full_name.encode().hex()}",'
                    f' {message.chat.id}, {int(time())}, '
                    f'"{message_text.encode().hex()}", {message.id}'
                    ')'
                )
                await _DB.commit()
            except BaseException as errorText:
                logger.syncLogger(
                    message=errorText,
                    module='TIME-CHECKER'
                )

    async def databaseRemove(
            self, message: Message | None = None,
            user_id: int | None = None,
            chat_id: int | None = None
        ) -> None:
        if message:
            chat_id = message.chat.id
            user_id = message.from_user.id

        if await self.checkDBexists(user_id, chat_id):
            async with connect(db) as _DB:
                await _DB.execute(
                    'DELETE FROM users WHERE '
                    f'id = {user_id} AND '
                    f'chat_id = {chat_id}'
                )
                await _DB.commit()


def getChat(message: Message) -> bool:
    if message.from_user.id != bot_id:
        return False
    if message.chat.id > 0:
        return False
    return True


@bot.message_handler(
    content_types=['new_chat_members', 'supergroup_chat_created'],
)
async def Hello(message: Message):
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.id == bot_id:
                await bot.send_message(
                    message.chat.id,
                    'Отлично. Для запуска бота, '
                    'выдайте ему права администратора чата, '
                    'после чего пропишите комманду /activate\n'
                    'Это необходимо для получения списка пользователей '
                    'а также чтения сообщений.'
                )


@bot.message_handler(commands=['activate'])
async def activateBot(message: Message) -> None:
    if message.chat.id > 0:
        return

    if message.from_user.id == checker_id:
        return

    await bot.send_message(message.chat.id, 'Бот активирован.')


@bot.message_handler(commands=['help'])
async def botHelp(message: Message) -> None:
    await bot.send_message(
        message.chat.id,
        'Счётчик игнора: Необходимая вещь при баттлах на дд. '
        'С его помощью будет проще понять, '
        'проиграл ли оппонент на баттле, или нет.\n'
        'Для начала работы бота, '
        'пригласите его в чат и выдайте ему права администратора, '
        'после чего пропишите /activate. Всё, бот запущен! '
        'Как только оппонент "покажет" более 3600 секунд (час) игнора, '
        'в чат будет отправлено соответствующее уведомление. Удачи!'
    )

    if message.from_user.id == checker_id:
        return

    if message.chat.id < 0:
        await DB().databaseAdd(message)


@bot.message_handler(commands=['copyright'])
async def cr(message: Message) -> None:
    await bot.send_message(
        message.chat.id,
        'IgnoreChecker, developed by #rvze, 2024.\n'
        'Contacts:\n'
        '<pre>\n'
        '    TG: @imdoxx\n'
        '    VK: vk.com/internetrvze\n'
        '</pre>\n'
        'Telegram Channels: @TrushniyDoxbin | @chimerattak'
    )

    if message.from_user.id == checker_id:
        return

    if message.chat.id < 0:
        await DB().databaseAdd(message)


@bot.message_handler(content_types=[
    'video', 'text', 'audio', 'document', 'photo',
    'sticker', 'voice', 'video_note', 'location', 'contact'
], func=lambda message: message.chat.id < 0
)
async def mainHandler(message: Message) -> None:
    if message.from_user.id == checker_id:
        return

    await DB().databaseAdd(message)


@bot.message_handler(
        content_types=['left_chat_member'],
        func=lambda message: message.from_user.id == bot_id
    )
async def leaveAndKickHandler(message: Message) -> None:
    await DB().datavaseRemove(message)


async def checker() -> None:
    while True:
        async with connect(db) as _DB:
            database = await _DB.execute_fetchall('SELECT * FROM users')
            try:
                for data in database:
                    if data[3] + 3600 - int(time()) <= 0:

                        await bot.send_message(
                            data[2],
                            '<b>Час игнора от пользователя!</b>\n'
                            '👤 Пользователь: '
                            f'<a href="tg://user?id={data[0]}">'
                            f'{bytes.fromhex(data[1]).decode()}</a>\n'
                            f'⏱️ AFK: {int(time()) - data[3]} секунд.\n'
                            f'✍️ Последнее сообщение:'
                            f' {bytes.fromhex(data[4]).decode()}',
                            parse_mode='HTML'
                        )

                        await DB().databaseRemove(user_id=data[0], chat_id=data[2])

                await sleep(30)
            except BaseException as errorText:
                await logger.asyncLogger(
                    message=errorText, module='TIME-CHECKER'
                )


async def _() -> None:
    while True:
        try:
            await _gather(
                checker(), bot.polling(non_stop=True),
            )

        except BaseException as errorText:
            await logger.asyncLogger(
                message=errorText, module='TIME-CHECKER'
            )


_runner(_())
