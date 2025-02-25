## Задание
Авторизация.
Реализовать систему авторизацию (JWT )с поддержкой авторизации через Yandex.
Организовать ролевую модель и историю заходов с помощью этой авторизации.
При регистрации, необходимо отправлять письмо в телеграм чат с приветственным сообщением. 
Для этого нужно написать воркер,  который слушает события
из кафки и отправляет сообщение пользователю.

![Снимок экрана 2025-02-25 110214](https://github.com/user-attachments/assets/6a56f58f-c75c-42f3-9882-d80c7794ad41)
![Снимок экрана 2025-02-25 110239](https://github.com/user-attachments/assets/1e2af1da-8b33-4524-bf58-67ae09f6ddde)
![Снимок экрана 2025-02-25 110305](https://github.com/user-attachments/assets/d32a1500-f63f-48a9-9020-4bc57058c9f1)

![image](https://github.com/user-attachments/assets/a5f681ee-c125-4d23-8343-0a8e9ce61a0f)


### Для запуска

make app - запустить все контейнеры

make app-down - выключить контейнеры

make auth-shell - зайти в shell auth контейнера

make bot-shell - зайти в shell bot контейнера

make auth-logs - просмотреть логи auth

make bot-logs - просмотреть логи bot

Необходимо создать SSL сертификат и ключ для подключения по https

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

(Ключ и сертификат надо добавить в AuthService/app)

