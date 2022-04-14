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
### Running the PostgreSQL Database
Run the Docker image you just created to run the PostgreSQL server. Give a name to the container using `<CONTAINER NAME>`, and specify what port you want to use when accessing the database.
```bash
docker run --name <CONTAINER NAME> -p <PORT>:5432 -d <IMAGE NAME>
```
The Dockerfile specifies the following defaults:
* Database: `msd_db`
* Username: `db_user`
* Password: `LetMeIn`  
 
The Docker container will take about 15 - 20 minutes to fully get running the first time before being able to access the database as it initializes the PostgreSQL database with the song data.

Once you have run the Docker image and created a container, you can freely start and stop the container without having to recreate the container again using the following commands:
```bash
docker start <CONTAINER NAME>
docker stop <CONTAINER NAME>
````
## Data

Provided by The Echo Nest. [The Echo Nest](https://en.wikipedia.org/wiki/The_Echo_Nest) is a music intelligence and data platform for developers and media companies owned by Spotify. 

| **Field**                                              | **Type**       | **Description**                               |
|--------------------------------------------------------|----------------|-----------------------------------------------|
| track_id                                               | string         | Echo Nest track ID                            |
| song_id                                                | string         | Echo Nest song ID                             |
| title                                                  | string         | song title                                    |
| track_7digitalid                                       | int            | ID from 7digital.com or -1                    |
| analysis_sample_rate                                   | float          | sample rate of the audio used                 |
| audio_md5                                              | string         | audio hash code                               |
| danceability                                           | float          | algorithmic estimation of danceability        |
| duration                                               | float          | in seconds                                    |
| end_of_fade_in                                         | float          | seconds at the beginning of the song          |
| energy                                                 | float          | energy from listener point of view            |
| key                                                    | int            | key the song is in                            |
| key_confidence                                         | float          | confidence measure                            |
| loudness                                               | float          | overall loudness in dB                        |
| mode                                                   | int            | major or minor                                |
| mode_confidence                                        | float          | confidence measure                            |
| start_of_fade_out                                      | float          | time in sec                                   |
| tempo                                                  | float          | estimated tempo in BPM                        |
| time_signature                                         | int            | estimate of number of beats per bar, e.g. 4   |
| time_signature_confidence                              | float          | confidence measure                            |
| bars_confidence                                        | array float    | confidence measure                            |
| bars_start                                             | array float    | beginning of bars, usually on a beat          |
| beats_confidence                                       | array float    | confidence measure                            |
| beats_start                                            | array float    | result of beat tracking                       |
| sections_confidence                                    | array float    | confidence measure                            |
| sections_start                                         | array float    | largest grouping in a song, e.g. verse        |
| segments_confidence                                    | array float    | confidence measure                            |
| segments_loudness_max                                  | array float    | max dB value                                  |
| segments_loudness_max_time                             | array float    | time of max dB value, i.e. end of attack      |
| segments_loudness_start  (segments loudness max start) | array float    | dB value at onset                             |
| segments_pitches                                       | 2D array float | chroma feature, one value per note            |
| segments_start                                         | array float    | musical events, ~ note onsets                 |
| segments_timbre                                        | 2D array float | texture features (MFCC+PCA-like)              |
| tatums_confidence                                      | array float    | confidence measure                            |
| tatums_start                                           | array float    | smallest rythmic element                      |
| artist_terms                                           | array string   | Echo Nest tags                                |
| artist_terms_freq                                      | array float    | Echo Nest tags freqs                          |
| artist_terms_weight                                    | array float    | Echo Nest tags weight                         |
| similar_artists                                        | array string   | Echo Nest artist IDs (sim. algo. unpublished) |
| artist_7digitalid                                      | int            | ID from 7digital.com or -1                    |
| artist_familiarity                                     | float          | algorithmic estimation                        |
| artist_hotttnesss                                      | float          | algorithmic estimation                        |
| artist_id                                              | string         | Echo Nest ID                                  |
| artist_latitude                                        | float          | latitude                                      |
| artist_longitude                                       | float          | longitude                                     |
| artist_location                                        | string         | location name                                 |
| artist_mbid                                            | string         | ID from musicbrainz.org                       |
| artist_name                                            | string         | artist name                                   |
| artist_playmeid                                        | int            | ID from playme.com, or -1                     |
| genre                                                  |                |                                               |
| release                                                | string         | album name                                    |
| release_7digitalid                                     | int            | ID from 7digital.com or -1                    |
| song_hotttnesss                                        | float          | algorithmic estimation                        |
| artist_mbtags                                          | array string   | tags from musicbrainz.org                     |
| artist_mbtags_count                                    | array int      | tag counts for musicbrainz tags               |
| year                                                   | int            | song release year from MusicBrainz or 0       |

## Authors and Acknowledgments
Michael Salceda  
Sean Kim
