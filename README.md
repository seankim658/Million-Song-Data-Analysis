# EMSE 6586 Million Song Data Analysis

This project repo is for Michael Salceda and Sean Kim. This holds our EMSE 6586 final project: an exploration and analysis of the Million Song dataset (http://millionsongdataset.com/). Due to the size of data available in the entire Million Song dataset, we are only using the Million Song Subset dataset which has 10,000 songs versus the full 1,000,000 songs.

## Description
...

## Installation
1. Install Docker on your machine (https://docs.docker.com/get-docker/).
2. Clone this repository to your machine.
3. Build the custom Docker image from the included Dockerfile. Fill in `IMAGE NAME` with whatever Docker image name you want, and fill in `<PATH/TO/DOCKERFILE>` with the proper path to the Dockerfile from whatever directory you are working from.
```bash
docker image build -t <IMAGE NAME> <PATH/TO/DOCKERFILE>
```
4. Create a `conda` environment using the `conda_environment.yml` file and activate the environment.
```bash
conda env create -f <PATH/TO/conda_environment.yml>
conda activate EMSE6586
````

## Usage
1. Run the Docker image you just created to run the PostgreSQL server. Give a name to the container using `<CONTAINER NAME>`, and specify what port you want to use when accessing the database.
```bash
docker run --name <CONTAINER NAME> -p <PORT>:5432 -d <IMAGE NAME>
```
The Dockerfile specifies the following defaults:
* Database: `msd_db`
* Username: `db_user`
* Password: `LetMeIn`  

The Docker container will take about 15 - 20 minutes to fully get running before being able to access the database as it initializes the PostgreSQL database with the song data.

## Authors and Acknowledgments
Michael Salceda  
Sean Kim
