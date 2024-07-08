from telethon import TelegramClient, events
from telethon.types import Message
from dotenv import load_dotenv
from os import getenv
from sys import version_info as version
from aiosqlite import connect
from time import time
from logger import Logger


__version__ = '1.1'
__enviromentVersion__ = f'{version.major}.{version.minor}.{version.micro}'


load_dotenv()
userbot = TelegramClient(
    session=getenv('SESSION_FILE_NAME'), api_id=int(getenv('API_ID')),
    api_hash=getenv('API_HASH'),
    system_version=f'Python Enviroment v{__enviromentVersion__}',
    app_version='#rvze Time Checker',
).start()
db = getenv('DATABASE_PATH')
logger = Logger()


async def checkDBexists(id: int, chat_id: int) -> bool:
    async with connect(db) as _DB:
        if len(
            await _DB.execute_fetchall(
                'SELECT id FROM users '
                f'WHERE chat_id={chat_id} AND id={id}'
            )
        ):
            return True
    return False


@userbot.on(events.NewMessage())
async def UserbotMainHandler(event: events.NewMessage.Event) -> None:
    message: Message = event.message
    entity = await userbot.get_entity(message.from_id.user_id)
    from_user = f'{entity.first_name} ' \
                f'{entity.last_name if entity.last_name else ''}'
    from_user = from_user.encode().hex()
    try:
        message_text: str = event.message.text
        message_text = message_text.encode().hex()
        sender = await event.get_sender()
        if sender.id == 7057834830:
            return

        if sender.bot:
            async with connect(db) as _DB:
                if await checkDBexists(
                    sender.id,
                    event.chat_id
                ):
                    await _DB.execute(
                        'UPDATE users SET '
                        f'last_message_time = {int(time())}, '
                        f'last_message_id = {event._message_id}, '
                        f'last_message_text = "{message_text}"'
                        f' WHERE id = {sender.id} '
                        f'AND chat_id = {event.chat_id}'
                    )
                    return await _DB.commit()
                await _DB.execute(
                    'INSERT INTO users ('
                    'id, full_name, chat_id, last_message_time, '
                    'last_message_text, last_message_id'
                    f') values ({sender.id}, "{from_user}",'
                    f' {event.chat_id}, {int(time())}, "{message_text}", '
                    f'{event._message_id}'
                    ')'
                )
                await _DB.commit()

    except BaseException as errorText:
        await logger.asyncLogger(
            message=errorText,
            module='USERBOT'
        )


if __name__ == '__main__':
    del getenv, load_dotenv, version

    try:
        userbot.run_until_disconnected()
    except BaseException as errorText:
        logger.syncLogger(
            message=errorText,
            module='USERBOT'
        )
