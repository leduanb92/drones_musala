DRONES: A REST API Application using Django REST Framework
===

This project uses [Django](https://www.djangoproject.com/) and [Django REST framework](http://www.django-rest-framework.org/) to provide a service via REST API to allow
clients to communicate with drones.


Description
----------

The application is a simple RESTful app that stores `drones` and `medications` and allows to create and retrieve them.
It also allows to get available drones to be loaded, to check battery level of a specific drone, to load one with specified medication items and to get loaded medication items from it. 
The project makes use of Docker to create neccessary containers to build and run the project in a simple way

It uses python 3.8, Django 4.1.2, DRF 3.14 and requires Docker 17


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
    └── (Files defining models, serializers, views and other needed resources)

```



Instructions to build and run
-----------------------------

The docker-compose file has all the services to run the project. Just follow these steps:

- First open a terminal and move to the root folder of the project.
- Now run the command `docker-compose build` to build the image.
- Finally, run `docker-compose up [-d]`. The `-d` parameter is optional, it allows to run the process in _detach_ mode.

You can go and visit the [Browsable API](http://localhost:8000) to see and browse the endpoints, or you can interact with it using any tool of your preference like **Postman**.

You can also see the API documentation [here with Swagger-UI](http://localhost:8000/api-docs/swagger) or [here with ReDoc](http://localhost:8000/api-docs/redoc).

Instructions to run tests
-----------------------------
There are implemented unit tests for all the main functionalities specified in the exercise. They are located
in `drones/tests.py`. To run them, just open a terminal and execute the following command:

`docker exec -it drones_app python3 /app/manage.py test`.

You will see the results in your terminal
