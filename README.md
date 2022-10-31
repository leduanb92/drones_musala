DRONES: A REST API Application using Django REST Framework
===

This project uses [Django](https://www.djangoproject.com/) and [Django REST framework](http://www.django-rest-framework.org/) to provide a service via REST API to allow
clients to communicate with drones.


Description
----------

The application is a simple RESTful app that stores `drones` and `medications` and allows to create and retrieve them.
It also allows to get available drones to be loaded, to check battery level of a specific drone, to load one with specified
medication items and to get loaded medication items from it. 
**Redis** is used in conjunction with **Celery** to schedule the periodic task to check and log the battery level of the drones.
As the Database is used **SQLite** as it is a small project and its only purpose is to develop the exersice requirements. 
The project makes use of Docker to create necessary containers to build and run the project in a simple way

It uses python 3.8, Django 4.1.2, DRF 3.14.


Tree structure
--------------

```
├── README.md (this file)
├── docker-compose.yaml (general dockerfile description)
├── Dockerfile (General Dockerfile of the main server)
├── requirements.txt (python requirements)
├── manage.py (Django's command-line utility for administrative tasks)
├── drones_musala (project main folder, contains settings and other important files
│   └── settings.py (settings of the project)
│   └── urls.py (configuration of API routes)
│   └── celery.py (celery app to run periodic task)
│   └── ...
├── drones (main django app)
    └── (Files defining models, serializers, views, tests and other needed resources)

```


Instructions to build and run
-----------------------------

The docker-compose file has all the services to run the project. Just follow these steps:

- First open a terminal and move to the root folder of the project.
- Now run the command `docker-compose build` to build the image.
- Finally, run `docker-compose up [-d]`. The `-d` parameter is optional, it allows to run the process in _detach_ mode.


### Run project without using Docker
If you don't want to use Docker, you can run the project manually. First of all make sure you have installed `Python 3.8+`,
`Redis 6.0+` and that `redis-server` is running. Then go to the project root, open a terminal and follow the next steps:
- First create a virtual environment to install the project's dependencies, for that execute this command:  
    ```python3 -m venv env```
- Now activate the virtual environment you just created with:  
    ```source env/bin/activate```
- Next you have to install the dependencies needed. Type this in your terminal and execute it:  
    ```python3 -m pip install -r requirements.txt```
- Now you can run the django server to interact with the API, for that run this:  
    ```python3 manage.py runserver 0.0.0.0:8000```
- Finally, open another terminal and run the next commands to start the celery worker:  
    1- ```export DJANGO_SETTINGS_MODULE=drones_musala.settings```  
    2- ```celery -A drones_musala worker -l info```  

That's all, you already can go and visit the [Browsable API](http://localhost:8000) to see and browse the endpoints, or 
you can interact with it using any tool of your preference like **Postman**.  
You can also see the API documentation [here, with Swagger-UI,](http://localhost:8000/api-docs/swagger) or [here, with ReDoc](http://localhost:8000/api-docs/redoc).


Instructions to run tests
-----------------------------
There are implemented unit tests for all the main functionalities specified in the exercise. They are located
in `drones/tests.py`. To run them, just open a terminal and execute the following command:  

- `docker exec -it drones_app python3 /app/manage.py test`.  

**NOTE:** If you **did not** use Docker to run the project, then execute this in the root folder of the project with the
virtual environment activated:  
`python3 manage.py test`

You will see the results in your terminal
