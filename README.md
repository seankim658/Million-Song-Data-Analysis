# EMSE 6586 Million Song Data Analysis

This project repo is for Michael Salceda and Sean Kim. This holds our EMSE 6586 final project: an exploration and analysis of the Million Song dataset (http://millionsongdataset.com/).

## Description
...

## Installation
1. Install Docker on your machine (https://docs.docker.com/get-docker/).
2. Clone this repository to your local machine.
3. Build the custom Docker image from the included Dockerfile. Fill in `IMAGE NAME` with whatever Docker image name you want and fill in `<PATH/TO/DOCKERFILE>` with the proper path to the Dockerfile from whatever directory you are working from.
```bash
docker image build -t <IMAGE NAME> <PATH/TO/DOCKERFILE>
````
4. Run the Docker image you just created to run the PostgreSQL server. Give a name to the container using `<CONTAINER NAME>` and supply a default password for PostgreSQL. **NOTE**: You MUST supply a default password or else it will fail to start the PostgreSQL server.
```bash
docker run --name <CONTAINER NAME> -e POSTGRES_PASSWORD=<PASSWORD> -p 5432:5432 -d <IMAGE NAME>
```

## Usage
...

## Authors and acknowledgment
Michael Salceda
Sean Kim
