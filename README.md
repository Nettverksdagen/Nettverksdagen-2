# Nettverksdagen 2.0

## Prerequisites
Note! Depending on your setup, you might need to use `python3` and `pip3` instead of `python` and `pip`. **It's very important that the project is ran with python 3 and not 2.7!**

### Install pip
```bash
sudo apt install python-pip # Ubuntu based linux
sudo brew install python-pip # OSX
```

### Install virtualvenv
Note: installing virtualenv with a python2 installation of pip, is not recommended.
```bash
pip install virtualenv
```

### Install Vue CLI (optional)
Vue CLI is used to configure the codebase easily
```bash
npm i -g @vue/cli
```

## Project Installation
### 1. Clone the repo
```bash
git clone https://github.com/Nettverksdagen/Nettverksdagen-2.git
cd nvd-new
```

### 2. Set up and enter virtual environment
```bash
virtualenv venv
source venv/bin/activate
```
Note: If virtualvenv is set up to use python2, you can specify python3 as the correct version with
```bash
virtualvenv venv -p /path/to/python3/executable
```

### 3. Install python deps
```bash
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install django-rest-auth
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
