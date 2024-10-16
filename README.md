# WEB-app "Foodgram"
### for viewing and publishing recipes

Features of the application:

- Publish your own recipes  
- Add others' recipes to favorites  
- Follow publications from other authors  
- Add recipes to shopping carts and download the ingredient list as a PDF file  

## Technology stack:
 [![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=e8b600&color=065535)](https://docs.python.org/release/3.9.10)

 [![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=065535 )](https://www.djangoproject.com/)

 [![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=3d85c6)](https://www.postgresql.org/)


### Recommendations for deploying the project locally

Clone the project:

```bash
git clone https://github.com/Romaizega/foodgram-project-react.git
```

Navigate to the project folder:

```bash
cd foodgram-project-react.git
```

Install a virtual environment:

linux
```bash
python3 -m venv env
```
windows
```bash
python -m venv venv
```
Activate the virtual environment:

linux
```bash
source venv/bin/activate
```
windows
```bash
source venv/Script/activate
```
Install dependencies:

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

+ Install locally. [Docker compose](https://www.docker.com/)
+ Create `.env` files in the `backend` and `infra-dev` folders
```
POSTGRES_USER=foodgram_user
POSTGRES_DB=django
POSTGRES_PASSWORD=foodgram_password
DB_HOST=db
SECRET_KEY=(SECRET_KEY)
ALLOWED_HOSTS=(ALLOWED_HOSTS)
DEBUG=False
```
+ Run the project using `docker compose up`:
```shell script
cd foodgram-project-react/infta-dev
```

```shell script
docker compose  up --build
```


+Run the backend server:
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
Documentation is available at the following address http://localhost/api/docs/ 


### Recommendations for deploying the project on a server:

Clear the npm cache
```shell script
npm cache clean --force
```
Clear the APT cache
```shell script
sudo apt clean
```
Clear old system logs
```shell script
 sudo journalctl --vacuum-time=1d
```
Install Docker Compose 
```shell script
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin
```
Configure Nginx on the server:
```shell script
sudo apt install nginx -y
```

```shell script
sudo systemctl start nginx
```

```shell script
sudo nano /etc/nginx/sites-enabled/default
```

+ Add configurations:
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

+ Check functionality:
```shell script
sudo systemctl status nginx
```

Obtain an `SSL` certificate:
+ Configure `Firewall`:
```shell script
sudo ufw allow 'Nginx Full'
```

```shell script
sudo ufw allow OpenSSH
```

```shell script
sudo ufw enable
```
Working with the directory on the remote server:
+ Create a directory:
```shell script
mkdir foodgram/
```
+ Create a directory inside: `foodgram`:
```shell script
mkdir infra/
```

+ Create `.env`, `docker-compose.production.yml`, `nginx.conf` in the directory `foodgram/infra/`:


+ Navigate to the directory:
```shell script
cd foodgram/infra/
```
Starting the project on the server:
+ Starting `Docker` containers:
```shell script
scp -i sudo docker compose -f docker-compose.production.yml up -d
```
+ Configure `Backend`:
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

+ Upload the list of ingredients to the database:
```shell script
sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients
```

+ Check that the containers are running:
```shell script
scp -i sudo docker compose -f docker-compose.production.yml ps
```


### Access to the project:

[![FOODGRAM](https://img.shields.io/badge/-FOODGRAM-000000?style=flat&color=008080)](https://foodgramenjoy.ddns.net)



### Author:
[Roman Izegov](https://github.com/Romaizega)
