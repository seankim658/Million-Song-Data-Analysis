############
# Built-in #
############
import csv
from io import StringIO
import os
import re

###############
# Third-party #
###############
import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Defining global variables
HOST = '/var/run/postgresql/'
USER = 'db_user'
PORT = 5432
DATABASE = 'msd_db'
PASSWORD = 'LetMeIn'

def convert_h5_to_df(filepath='./MillionSongSubset/'):
    '''Convert H5 files located at the specified filepath to a DataFrame.

    Parameters
    ----------
    filepath : str
        Path to folder containing H5 files

    Returns
    -------
    tracks_df : DataFrame
        pandas DataFrame with converted H5 data
    '''
    file_num = 1
    tracks_df = pd.DataFrame()

    # Iterate through filepath to get to H5 files
    for root, dirs, files in os.walk(filepath):
        path = root.split(os.sep)
        for file in files:
            print(f'Processing {file} ({file_num}/10000)...', end = '')

            # Need to wrap processing in context manager to make sure H5 
            # files get closed once done or else it will error out with 
            # too many open files
            full_path_str = f'{"/".join(path)}/{file}'
            with pd.HDFStore(full_path_str, 'r') as curr_track:
                df_list = []
                
                # The Million-Song dataset has three "nodes" of data,
                # each with their own set of attributes to pull out
                for node in ['analysis', 'metadata', 'musicbrainz']:
                    for attribute in curr_track.get_node(node):
                        attr_name = attribute.name
                        try:
                            # If the H5 type is a Table, this will run 
                            # properly. Otherwise, it will fail and 
                            # fallback to treating each node as a 
                            # separate entity
                            df_list.append(
                                curr_track.get(f'/{node}/{attr_name}/')
                            )
                        except:
                            numpyized_data = np.array(
                                curr_track.get_node(node)[attr_name]
                                )
                            if numpyized_data.shape[0] > 0:
                                # Treat string fields differently - need
                                # to convert to either UTF-8 or Latin-1 
                                # (if UTF-8 fails) before putting it into
                                # a DataFrame or else it will look weird
                                # in PostgreSQL
                                if attr_name in [
                                    'artist_mbtags', 
                                    'artist_terms', 
                                    'similar_artists'
                                ]:
                                    # This regex replaces single-quotes with
                                    # double-quotes so it parses correctly
                                    # in PostgreSQL while avoiding singleton
                                    # single-quotes like that found in "rock 'n roll"
                                    pattern = re.compile(
                                        r'(?:(?<!\w)\'((?:.|\n)+?\'?)(?:(?<!s)\'(?!\w)|(?<=s)\'(?!([^\']|\w\'\w)+\'(?!\w))))'
                                    )
                                    substitute = "\"\g<1>\""

                                    # We need to create a string representation
                                    # of the array data for PostgreSQL to
                                    # parse the data correctly into the database
                                    try:
                                        str_repr = re.sub(
                                            pattern,
                                            substitute,
                                            str(
                                                np.char.decode(
                                                    numpyized_data, 
                                                    'utf-8'
                                                ).tolist()
                                            ).replace('[', '{') \
                                            .replace(']', '}') \
                                            # this replacements below is necessary 
                                            # to make the regex search work
                                            .replace('\'n\'', '\'n') \
                                            .replace('"', '\'')
                                        )
                                    except UnicodeDecodeError:
                                        str_repr = re.sub(
                                            pattern,
                                            substitute,
                                            str(
                                                np.char.decode(
                                                    numpyized_data, 
                                                    'latin-1'
                                                ).tolist()
                                            ).replace('[', '{') \
                                            .replace(']', '}') \
                                            # this replacements below is necessary 
                                            # to make the regex search work
                                            .replace('\'n\'', '\'n') \
                                            .replace('"', '\'')
                                        )

                                    df_list.append(
                                        pd.DataFrame({
                                            attr_name: [str_repr]
                                        })
                                    )
                                else:
                                    df_list.append(
                                        pd.DataFrame({
                                            attr_name: [
                                                str(numpyized_data.tolist()) \
                                                    .replace('[', '{') \
                                                    .replace(']', '}')
                                            ]
                                        })
                                    )
                            else:
                                df_list.append(
                                    pd.DataFrame({
                                        attr_name: [
                                            str(numpyized_data.tolist()) \
                                                .replace('[', '{') \
                                                .replace(']', '}')
                                        ]
                                    })
                                )

            tracks_df = pd.concat(
                [tracks_df, pd.concat(df_list, axis = 1)], 
                ignore_index = True
            )
            file_num += 1
            print('done!')

    return tracks_df

def create_songs_table(table_name='song_info'):
    '''Create table of song info in PostgreSQL database.

    Parameters
    ----------
    table_name : str
        Name of table to create in PostgreSQL database
    '''
    # Connect to the database using psycopg
    # for database creation
    psycopg_conn = psycopg2.connect(
        host = HOST,
        user = USER,
        port = PORT,
        database = DATABASE,
        password = PASSWORD
    )
    psycopg_conn.set_session(autocommit = True)
    psycopg_cur = psycopg_conn.cursor()

    delete_table_sql = f'''
        DROP TABLE IF EXISTS {table_name}
    '''

    create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS {table_name}(
            track_id VARCHAR PRIMARY KEY,
            song_id VARCHAR,
            title VARCHAR,
            track_7digitalid INT,
            analysis_sample_rate FLOAT,
            audio_md5 VARCHAR,
            danceability FLOAT,
            duration FLOAT,
            end_of_fade_in FLOAT,
            energy FLOAT,
            key INT,
            key_confidence FLOAT,
            loudness FLOAT,
            mode INT,
            mode_confidence FLOAT,
            start_of_fade_out FLOAT,
            tempo FLOAT,
            time_signature INT,
            time_signature_confidence FLOAT,
            bars_confidence NUMERIC[],
            bars_start NUMERIC[],
            beats_confidence NUMERIC[],
            beats_start NUMERIC[],
            sections_confidence NUMERIC[],
            sections_start NUMERIC[],
            segments_confidence NUMERIC[],
            segments_loudness_max NUMERIC[],
            segments_loudness_max_time NUMERIC[],
            segments_loudness_start NUMERIC[],
            segments_pitches NUMERIC[][],
            segments_start NUMERIC[],
            segments_timbre NUMERIC[][],
            tatums_confidence NUMERIC[],
            tatums_start NUMERIC[],
            artist_terms VARCHAR[],
            artist_terms_freq NUMERIC[],
            artist_terms_weight NUMERIC[],
            similar_artists VARCHAR[],
            artist_7digitalid INT,
            artist_familiarity FLOAT,
            artist_hotttnesss FLOAT,
            artist_id VARCHAR,
            artist_latitude FLOAT,
            artist_longitude FLOAT,
            artist_location VARCHAR,
            artist_mbid VARCHAR,
            artist_name VARCHAR,
            artist_playmeid INT,
            genre VARCHAR,
            release VARCHAR,
            release_7digitalid INT,
            song_hotttnesss FLOAT,
            artist_mbtags VARCHAR[],
            artist_mbtags_count INT[],
            year INT
        )
    '''

    # Just adopting a strategy of deleting
    # and recreating the table to avoid
    # any data issues
    print('Deleting existing table...', end = '')
    psycopg_cur.execute(delete_table_sql)
    print('done!')
    print('Creating table...', end = '')
    psycopg_cur.execute(create_table_sql)
    print('done!')

    psycopg_cur.close()
    psycopg_conn.close()

    print(f'Table "{table_name}" successfully created!')

def insert_data(df, table_name='song_info'):
    '''Insert pandas DataFrame data into PostgreSQL table.

    Parameters
    ----------
    df : DataFrame
        pandas DataFrame containing data to insert into table

    table_name : str
        Name of the table to insert into
    '''
    def _psql_insert_copy(table, conn, keys, data_iter):
        '''Helper function to execute SQL statement inserting data to PostgreSQL.

        Code taken from https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql-method
        since default way of using `to_sql` is too slow on inserts.

        Parameters
        ----------
        table : pandas.io.sql.SQLTable
        conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
        keys : list of str
            Column names
        data_iter : Iterable that iterates the values to be inserted
        '''
        dbapi_conn = conn.connection
        with dbapi_conn.cursor() as cur:
            s_buf = StringIO()
            writer = csv.writer(s_buf)
            writer.writerows(data_iter)
            s_buf.seek(0)

            columns = ', '.join([f'"{k}"' for k in keys])
            if table.schema:
                table_name = f'{table.schema}.{table.name}'
            else:
                table_name = table.name

            sql = f'COPY {table_name} ({columns}) FROM STDIN WITH CSV'
            cur.copy_expert(sql = sql, file = s_buf)

    # Connect with SQLAlchemy
    print('Creating SQLAlchemy connection engine...', end = '')
    conn_string = f'postgresql://{USER}:{PASSWORD}@{PORT}/{DATABASE}?host={HOST}'
    sqla_conn = create_engine(conn_string)
    print('done!')

    # Get a list of columns of the table created to make sure we only
    # add those columns - otherwise, PostgreSQL will complain
    print('Getting list of columns to use...', end = '')
    col_list = pd.read_sql(
        f'''
            SELECT 
                column_name 
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_name = '{table_name}'
        ''',
        sqla_conn
    )['column_name'].tolist()
    print('done!')

    # Push DataFrame into the database
    print('Inserting data into database...', end = '')
    df[col_list].to_sql(
        table_name, 
        sqla_conn, 
        if_exists = 'append', 
        method = _psql_insert_copy, 
        index = False, 
        chunksize = 1000
    )
    print('done!')

if __name__ == '__main__':
    print('TABLE CREATION'.center(50, '='))
    create_songs_table()

    print('FILE CONVERSION'.center(50, '='))
    tracks_df = convert_h5_to_df()

    print('DATA INSERTION'.center(50, '='))
    insert_data(tracks_df)

    print('Database seeding complete!')
