# Extensional-discord-bot

## Добавление бота на discord-сервер

1. Создать приложение:
    1. Перейти по ссылке: https://discord.com/developers/applications
    1. В правом верхнем углу нажать кнопку "New Application"
    1. Во всплывшем окошке ввести желаемое название приложения
1. Создать бота:
    1. Перейти в приложение, выбрав его из списка: https://discord.com/developers/applications
    1. Слева нажать на вкладку "Bot", затем нажать кнопку "Add bot"
    1. Сгенерировать токен, нажав кнопку "Regenerate token". Этот токен нужно указать в конфиг-файле [example.env](example.env).
    1. На той же странице, в разделе "Bot Permissions", отметить нужные привелегии, например "Administrator". Изменения необходимо сохранить.

## Ссылки

- Документация модуля discord.py:
    https://discordpy.readthedocs.io/en/latest/index.html
- Документация для разработчиков:
    https://discord.com/developers/docs/intro
