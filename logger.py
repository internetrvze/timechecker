from telebot.async_telebot import AsyncTeleBot
from asyncio import run as _runner
from functools import lru_cache
from dotenv import load_dotenv
from datetime import datetime
from os import getenv


class ParseMode:
    HTML = 'HTML'
    markdown = 'markdown'
    markdownV2 = 'markdownV2'


class LoggingLevel:
    DEBUG = 'DEBUG'
    ERROR = 'ERROR'
    INFO = 'INFO'
    CRITICAL = 'CRITICAL'


class Logger():
    @lru_cache()
    def __init__(self) -> None:
        load_dotenv()
        self.logger = AsyncTeleBot(getenv('LOGGER_BOT_TOKEN'))
        self.chat_id = int(getenv('LOGS_RECEIVER_ID'))
        self.logTime = ''

    def syncLogger(
        self, message: str, module: str,
        log_level: LoggingLevel = LoggingLevel.ERROR,
        parse_mode: ParseMode = 'HTML',
        with_time: bool = True,
    ) -> None:
        if with_time:
            self.logTime = datetime.now()
            day = str(self.logTime.day)
            year = str(self.logTime.year)
            month = str(self.logTime.month)
            hour = str(self.logTime.hour)
            minute = str(self.logTime.minute)
            second = str(self.logTime.second)

            month = f'0{month}' if int(month) < 10 else month
            day = f'0{day}' if int(day) < 10 else day
            minute = f'0{minute}' if int(minute) < 10 else minute
            second = f'0{second}' if int(second) < 10 else second

            self.logTime = f'[{day}.{month}.{year}] [{hour}:{minute}:{second}]'

        try:
            _runner(
                self.logger.send_message(
                    self.chat_id,
                    f'{self.logTime} {module}: {log_level}: {message}',
                    parse_mode=parse_mode
                )
            )
            return True
        except BaseException as error:
            print(f'Exception was ocurred: {error}')
            return False

    async def asyncLogger(
        self, message: str, module: str,
        log_level: LoggingLevel = LoggingLevel.ERROR,
        parse_mode: ParseMode = 'HTML',
        with_time: bool = True
    ) -> bool:
        if with_time:
            self.logTime = datetime.now()
            day = str(self.logTime.day)
            year = str(self.logTime.year)
            month = str(self.logTime.month)
            hour = str(self.logTime.hour)
            minute = str(self.logTime.minute)
            second = str(self.logTime.second)

            month = f'0{month}' if int(month) < 10 else month
            day = f'0{day}' if int(day) < 10 else day
            minute = f'0{minute}' if int(minute) < 10 else minute
            second = f'0{second}' if int(second) < 10 else second

            self.logTime = f'[{day}.{month}.{year}] [{hour}:{minute}:{second}]'

        try:
            await self.logger.send_message(
                self.chat_id,
                f'{self.logTime} {module}: {log_level}: {message}',
                parse_mode=parse_mode
            )
            return True
        except BaseException as error:
            print(f'Exception was ocurred: {error}')
            return False
