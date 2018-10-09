# Nettverksdagen 2.0

## Prerequisites
You might need some packages such as the Vue CLI, `virtualenv`, `pip` of course and many others. Handle any missing ones as you go along.

## Installation
Depending on your setup, you might need to use `python3` and `pip3` instead of `python` and `pip`.
### 1. Clone the repo
```bash
git clone https://github.com/sigtot/nvd-new.git
cd nvd-new
```

### 2. Set up and enter virtual environment
```bash
virtualenv venv -p
source venv/bin/activate
```

### 3. Install python deps
```bash
pip install django
pip install djangorestframework
pip install django-cors-headers
```

### 4. Run through migrations
```bash
python manage.py migrate
```

### 5. Install Vue packages
```bash
cd frontend
npm install
```

## Usage
### Start Django backend
```bash
source venv/bin/activate
python manage.py runserver
```
### Start Vue frontend
```bash
cd frontend
npm run dev
```

### Migrations
Creating:
```bash
python manage.py makemigrations
```
Applying:
```bash
python manage.py migrate
```
## Other random things

### Curl examples with authentication
Login
```bash
curl -X POST http://127.0.0.1:8000/rest-auth/login/ -d "username=admin&password=1234"
```

Create a listing
```bash
curl -X POST  http://127.0.0.1:8000/api/listing/ -d "name=test&company_name=test company" -H 'Authorization: Token c56ddd032e56280827fdf4c7c2d5ab338c1a1133'
``` 
