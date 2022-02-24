The project has been tested with
 
```sh
Docker version 19.03.13, build 4484c46d9d
docker-compose version 1.27.4, build 40524192
```
1. Clone the repository. In the project root run the following command to initialize airflow and create a default user
	```sh
	docker-compose up airflow-init
	```
	The username:password will be `airflow:airflow`

2. Now run the following command to initialize all containers. `--build` flag makes sure the containers are built before launch. This flag is default for the first run. 
	```sh
	docker-compose up --build
	```
