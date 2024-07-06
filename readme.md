### Возможно, первый чекер для баттлов в Telegram.


# Установка
Для начала работы необходимо установить необходимые пакетысоздать сессию и получить 2 токена:
1. Токен самого чекера
2. Токен для бота с логами чекера

### Установка пакетов
> Для установки пакетов достаточно прописать `pip install -r requirements.txt`

### Где создать ботов?
> 1. Для начала переходим в @BotFather.
> 2. В BotFather прописываем /newbot
> 3. Придумываем имя боту и username_bot
> 4. После заполнения всех полей мы получим токен бота.
> ![image](https://github.com/internetrvze/timechecker/assets/65215768/f1cbd8b1-a865-4ddb-b682-9761ed820d51)
>
> Подобную процедуру необходимо повторить и для бота-логгера.

После создания ботов необходимо заиметь сессию аккаунта-чекера.
### На данный момент поддерживаются только сессии Telethon!

### Для чего нужен аккаунт?
> В случае, если на баттле будут использоваться боты, чекер может не срабатывать.
>
> Это происходит потому-что боты не могут видеть сообщения других ботов.

Теперь, после создания ботов и сессии аккаунта, необходимо заполнить файл ***.env***.
- Шаблон для заполнения .env:
```python
BOT_TOKEN = "Токен бота-чекера"
LOGGER_BOT_TOKEN = "Токен бота-логгера"
LOGS_RECEIVER_ID = "ID человека, который будет получать логи от бота-логгера"
DATABASE_PATH = "Путь, куда будет сохранаться база данных чекера."
SESSION_FILE_NAME = "Путь к файлу сессии"
API_ID = "Сюда числа из api_hash"
API_HASH = "Сюда числа из api_hash"
CHECKER_UB_ID = "ID юзербота-логгера"
```
- Пример:
```python
BOT_TOKEN = "7057834830:ABRSpffdmblfGDgbgfdng-AABkdkbh64de"
LOGGER_BOT_TOKEN = "6777697907:AAE-oifoifgigjk6523dpeEhJHNDSLhfds"
LOGS_RECEIVER_ID = "6633740790"
DATABASE_PATH = ".\\bot.db"
SESSION_FILE_NAME = ".\\main.session"
API_ID = "27898422"
API_HASH = "dfkaqtvlcnglekbnhlo5327n4b7jj3l7"
CHECKER_UB_ID = "6697333255"
```

# Всё, чекер готов к запуску!

### Перед запуском...
> Перед запуском пропишите в оба бота команду /start
> В случае ошибок в работе, бот не сможет отправить вам ошибки. если вы не сделаете это.
> 
> Также просим вас проверить соединение с сетью на стабильность.

Для запуска бота пропишите в консоли/командной строке `python runner.py`


### Как пользоваться чекером?
> Добавьте его и юзербот-чекер в чат, где будет идти баттл, после чего выдайте боту права администратора, чтобы он мог читать сообщения.
> Как только кто-то из оппонентов будет молчать более 3600 секунд (часа) в чате, вы получите соответствующее оповещение:
> ![[Pasted image 20240706103432.png]]





#### Changelog
> [31.06.2024] Стабильный билд. v0.1
> [01.07.2024] Логирование теперь перенесено в отдельный модуль. v0.2
> [01.07.2024] Теперь бот не отвечает на последнее сообщение пользователя, показавшего час игнора. v0.2.1
> [01.07.2024] Исправлено самообнаружение чекера. v0.2.2
> [04.07.2024] В базе данный теперь сохраняется строка с полным именем пользователя. v0.3
> [04.07.2024] Управление базой данных перенесено в отдельный класс. v0.4
> [04.07.2024] Поля с текстом сообщения и именем пользователя теперь будут кодироваться в HEX перед добавлением в базу данных. v0.5
> [04.07.2024] Теперь бот поддерживает сообщения с вложениями. v0.6
