# Публикация комиксов

Данный скрипт скачивает случайный комикс из Xkcd

### Как установить

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Переменные окружения

Для использования скрипта необходимо создать `.env` файл, и по примеру ввести все необходимые данные:
```
CLIENT_ID=......
ACCESS_TOKEN=......
GROUP_ID=......
```  

`CLIENT_ID` - Это ID приложения в вк.

`ACCESS_TOKEN` - Токен, который нужно будет получить, следуя [инструкции](https://vk.com/dev/implicit_flow_user).

`GROUP_ID` - Это ID группы, в которой будут выкладываться посты.
