1.создайте .env файл в дериктории с проектом
впишите переменные:

POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=fastapi_db
POSTGRES_HOST=db

2. запустите проект docker-compose up --build

3. зайдите в контейнире и запустите миграции
3.1 docker ps
3.2 docker exec -it CONTAINER_ID bash
3.3 alembic upgrade head

перейдите по адресу localhost:8000/docs

/questions_num/{qty}
в параметрах введите колличество вопросов

/create_user/{username}
в параметрах введите имя, в ответ вы получите id и token

/upload/{id}/{token}
в параметрах введите id и token, которые вы получили раннее и выберите wav файл,в ответ вы получите ссылку

/download/{id}
используйте раннее полученную ссылку
