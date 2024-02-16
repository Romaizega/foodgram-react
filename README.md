# WEB-приложение "Foodgram"
### для просмотра и публикации рецептов

Возможности приложения:

- публиковать свои рецепты
- добавлять чужие рецепты в избранное
- подписываться на публикации других авторов
- добавлять рецепты в корзины и скачивать список ингредиентов в PDF файле

## Стек технологий
 [![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=e8b600&color=065535)](https://docs.python.org/release/3.9.10)

 [![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=065535 )](https://www.djangoproject.com/)

 [![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=3d85c6)](https://www.postgresql.org/)


### Рекомендации по развертыванию проекта локально

Клонируем проект:

```bash
git clone https://github.com/Romaizega/foodgram-project-react.git
```

Переходим в папку с проектом:

```bash
cd foodgram-project-react.git
```

Установить виртуальное окружение:

linux
```bash
python3 -m venv env
```
windows
```bash
python -m venv venv
```
Активировать виртуальное окружение:

linux
```bash
source venv/bin/activate
```
windows
```bash
source venv/Script/activate
```
Установить зависимости:

linux
```bash
python3 -m pip install --upgrade pip
```
windows
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

+ Установить локально [Docker compose](https://www.docker.com/)
+ Создать файлы .env в папках backend и infra-dev 
```
POSTGRES_USER=foodgram_user
POSTGRES_DB=django
POSTGRES_PASSWORD=foodgram_password
DB_HOST=db
SECRET_KEY=(SECRET_KEY)
ALLOWED_HOSTS=(ALLOWED_HOSTS)
DEBUG=False
```
+ Запустить проект через `docker compose up`:
```shell script
cd foodgram-project-react/infta-dev
```

```shell script
docker compose  up --build
```


+ Запустить backend сервер:
```shell script
cd backend/
```
```shell script
python manage.py migrate
```
```shell script
python manage.py runserver
```
```shell script
python manage.py createsuperuser
```
Документация доступна по адресу http://localhost/api/docs/ 


### Рекомендации по развертыванию проекта на сервере

Очистите кеш npm
```shell script
npm cache clean --force
```
Очистите кеш APT
```shell script
sudo apt clean
```
Очистите старые системные логи
```shell script
 sudo journalctl --vacuum-time=1d
```
Устанавливаем Docker Compose 
```shell script
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin
```
Настроить `Nginx` на сервере:
```shell script
sudo apt install nginx -y
```

```shell script
sudo systemctl start nginx
```

```shell script
sudo nano /etc/nginx/sites-enabled/default
```

+ Добавить конфигурации:
```
server {
    server_name <your-ip> <your-domen>;
    server_tokens off;

    location / {
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:8000;
    }
}
```
```shell script
sudo nginx -t
```

```shell script
sudo service nginx reload
```

+ Проверить работоспособность:
```shell script
sudo systemctl status nginx
```

Получить `SSl` сертификат:
+ Настраить `Firewall`:
```shell script
sudo ufw allow 'Nginx Full'
```

```shell script
sudo ufw allow OpenSSH
```

```shell script
sudo ufw enable
```
Работа с директорией на удаленном сервере:
+ Создать директорию:
```shell script
mkdir foodgram/
```
+ Создать директорию внутри `foodgram`:
```shell script
mkdir infra/
```

+ Создать `.env`, `docker-compose.production.yml`, `nginx.conf` в директории `foodgram/infra/`:


+ Перейти в директорию:
```shell script
cd foodgram/infra/
```
Запуск проекта на сервере:
+ Запустить `Docker` контейнеры:
```shell script
scp -i sudo docker compose -f docker-compose.production.yml up -d
```
+ Настроить `Backend`:
```shell script
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

```shell script
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```

```shell script
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /app/static/
```

```shell script
sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

+ Загрузить список ингредиентов в базу данных:
```shell script
sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients
```

+ Проверить, что контейнеры работают:
```shell script
scp -i sudo docker compose -f docker-compose.production.yml ps
```


### Доступ к проекту:

[![FOODGRAM](https://img.shields.io/badge/-FOODGRAM-000000?style=flat&color=008080)](https://foodgramenjoy.ddns.net)



### Автор:
[Р.Г. Изегов](https://github.com/Romaizega)