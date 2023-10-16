import pymysql.cursors
import pandas as pd
from .raw_profile_extract import fugitive_profiles




def transform():
    """
    Remove duplicates from extracts.
    """
    df = pd.DataFrame(fugitive_profiles, columns=[
        'name',
        'alias',
        'sex',
        'height',
        'weight',
        'eyes',
        'hair',
        'distinguishing_marks',
        'nationality',
        'date_of_birth',
        'place_of_birth',
        'charges',
        'wanted_by',
        'status',
        'publication',
        'last_modified',
        'reward',
        'details',
        'caution',
        'remarks',
        'images',
        'link',
    ])
    print(df)


def load():
    """
    Save transformed data to database.
    """
    connection = pymysql.connect(
        host='localhost',
        user='user',
        password='password',
        database='fugitive_profile_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


    with connection:
        with connection.cursor() as cursor:
            # Create new record
            sql = "INSERT INTO "
