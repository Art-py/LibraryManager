# Проект “LibraryManager”
Описание: 

ПО для автоматизации библиотеки покрывает все кейсы от управления движениями книги, до административной части.


`Создаю проект исключительно для учебных целей. Посмотрим что будет.`

[RoadMap](documentation/roadmap.md#roadmap)

Для развертки проекта, открываем каталог [environment](environment)
копируем в нем пример файла настроек и сохраняем убрав слово example:
`.env.example -> .env`
`.env.postgresql.example -> .env.postgresql`
`.env.redis.example -> .env.redis`
указываем свои значения. 

Далее устанавливаем зависимости проекта: `poetry install`

Запуск в докере: 

- `make build`

- `make up`

Команды для работы с проектом перечислены в [Makefile](Makefile), 
показать весь список доступных команд: `make list`

Автор: [Артём](https://t.me/Art_py)
