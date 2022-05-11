# docker-hw4
 Docker Project Flask/Python Redis MariaDB

This project creates 4 containers using Docker Compose.
The four containers are:
- Nginx
- Redis
- MariaDB
- App (Flask with Python)

Nginx uses a standard image and loads a configuration file with a proxy to port 5000. This allows access to the Application container. 

Redis has no special configuration. This is using a standard image.

MariaDB initializes the environment using an image from lscr.io. This is also using Docker Secrets to obfuscate the passwords for root and the user. A single database is created and an init.sql file is passed to create the table within that database as well as grant permissions to the non-root user.

App builds an image using a Dockerfile. This also exposes the port to the host computer to access the web application. By default this is set to port 5001 on the localhost as port 5000 was taken on my machine. Edit this value in the docker-compose.yml file.
The Dockerfile uses a python image and copies all files into the /code folder. The environment is set to FLASK app.py and is set to run on 0.0.0.0. There is a reqs.txt file which installs all python requirements with pip to interface with redis and mariadb.

The actual application is built with Python. Configuration can be found in app.py.

To launch the containers, clone the repository to your computer and run the docker-compose file.

Example:
```
 mkdir test-app
 cd test-app
 git clone https://github.com/martinanaya/docker-hw4
 cd docker-hw4
 docker-compose up --build
```
(Note: --build is optional. This will enforce a rebuild if you change any parameters or configurations.)
