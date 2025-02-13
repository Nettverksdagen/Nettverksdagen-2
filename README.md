# Nettverksdagen 2.0
> We can only see a short distance ahead, but we can see plenty there that needs to be done. *– Alan Turing*

## Prerequisites
* [Docker](https://www.docker.com/)
* [Docker compose](https://docs.docker.com/compose/)

## Project Installation
With docker-compose installed, the project requires minimal setup for the development environment:
```bash
git clone https://github.com/Nettverksdagen/Nettverksdagen-2.git
cd Nettverksdagen-2
docker-compose up
```
The webpage should now appear on `localhost:8080` and the django REST api browser on `localhost:8000`. 

## Mail Setup
### Mail setup in development environment
https://ethereal.email can create fake credentials, and the service can show all emails that were attempted sent (without actually sending them). This is also mentioned in `postfix/.env.default`.

### Mail setup in production environment
If you want to be able to actually send emails:
- Copy `postfix/.env.default` to `postfix/.env`
- Replace values with credentials from our mail provider (currently Uniweb)

## Quick tour of docker and the container setup
### What is docker and how does it help us?
Docker is a containerization and virtualization platform that packs individual components of the complete system into small containers that can be easily deployed on different platforms. Each part of the system is run in its own little linux virtual machine with very minimal overhead. With `docker-compose`, setting up a large system with many docker containers can be made relatively painless.

In our case, we have both a single-page vue frontend, a django REST api and a PostgreSQL database. The setup of this 3-part system can through the use of docker be reduced to a single `docker-compose up` command. Deployments can also be simplified tremendously, especially as the system grows, and the development environment can be made to match the production environment much more closely.

### The setup
Starting the webpage with `docker-compose up` spins up four docker containers.
A [Vue js](https://vuejs.org/) single page web application, a [Django REST](https://www.django-rest-framework.org/) API that interfaces a [PostgreSQL](https://www.postgresql.org/) database and a simple file uploading/hosting server for handling image uploads.
The flow of communication between these four components are shown in the figure below.
![Docker container setup](https://i.imgur.com/A8LzwaW.png)
We can retrieve a list of the containers when they are running with the `ps` command:
```bash
docker ps
```
To enter one of the listed containers and have a look around, copy the name of the container in question from the previous output (or let docker autocomplete it for you with tab) and type 
```bash
docker exec -ti nettverksdagen-2_frontend_1_c27e85b4cd47 bash
```
replacing `nettverksdagen-2_frontend_1_c27e85b4cd47` with the name of your container.
This will put you in a familiar bash shell. As you will probably notice, this shell is very limited.
It does for example not come with a text-editor out of the box, but you can easily install one with `apt-get` if necessary. What is more, the `fileserver` container is based on a [scratch](https://hub.docker.com/_/scratch/) image and so it doesn't even have `bash`. You can however execute single commands with `docker exec` as above. So for example to list files, run: 
```bash
docker exec -ti nettverksdagen-2_fileserver_1_c27e85b4cd47 ls
```

### Volumes
Any folders defined under `volumes` in `docker-compose.yml` will be mirrored into the container. Thus, folders containing the project files, namely
* `api/nvdagen`
* `api/nvdnew`
* `frontend/src`
* `frontend/static`
* `frontend/test`

will have any changes made to them reflected in the docker container when when files are saved.
The frontend even has hot reloading enabled, which means the webpage doesn't need to be reloaded for changes made in `frontend/` to appear in the browser window.

## Usage
### Django REST: migrations and the database
Changes in the database need to be reflected in a database migration so that the database schema and any previous data can be updated to the new model correctly. The migrations have to be executed inside the docker container for the api, so to begin, we list the running docker containers with `docker ps` and enter the api container:
```bash
docker exec -ti nettverksdagen-2_api_1_137f29309c2e bash
```
If we then have made changes to the model, we can generate a new migration with
```bash
python manage.py makemigrations
```
and perform migrations with
```bash
python manage.py migrate
```
Note that the api container has python 3 installed as the default python version, so there is no need to run these commands with `python3`.

The data already in the database can be cleared with 
```bash
python manage.py flush
```
(warning: this will destroy all data)

New fixtures are loaded with
```bash
python manage.py loaddata fixtures.json
```

### Create superuser for the api
To create a superuser for the api, execute the following command in the api container:
```bash
python manage.py createsuperuser
```
You will then be guided through the process of creating the user. 

### Install new NPM packages
When installing a new npm package, the frontend container needs to be rebuilt.
This can be done with the following command:
```bash
docker-compose build --no-cache
```

### Restart the file server
```bash
docker-compose stop fileserver && docker-compose up --no-deps -d --build fileserver
```

## Admin user
The dev environment has a default admin user with the following credentials:

| Username | Password |
| -------- | -------- |
| admin    | 1234     |

## Other random things
### Curl examples with authentication
#### Login
```bash
curl -X POST http://127.0.0.1:8000/rest-auth/login/ -d "username=admin&password=1234"
```

#### Create a listing
```bash
curl -X POST  http://127.0.0.1:8000/api/listing/ -d "name=test&company_name=test company" -H 'Authorization: Token c56ddd032e56280827fdf4c7c2d5ab338c1a1133'
``` 
