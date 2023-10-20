import os
import sys
import csv
import django
# import pymysql.cursors
import pandas as pd


DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
RAW_DATA_EXTRACT_FILE_PATH = os.path.abspath(os.path.join(DIRECTORY_PATH, './data_extracts/raw_profile_extracts.csv'))

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from UnifiedFugitiveDatabase.models import FugitiveProfiles



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


def save_to_database():
    """
    Save transformed data to database.
    """


    with open(RAW_DATA_EXTRACT_FILE_PATH, 'r') as file:
        reader = csv.reader(file)
        next(reader) # Advance past header

        # Delete all instances to avoid duplication and to
        # keep the database with up-to-date profiles
        FugitiveProfiles.objects.all().delete()

        for row in reader:
            profile = FugitiveProfiles(
                name=row[0],
                alias=row[1],
                sex=row[2],
                height_in_cm=row[3],
                weight_in_kg=row[4],
                eyes=row[5],
                hair=row[6],
                distinguishing_marks=row[7],
                nationality=row[8],
                date_of_birth=row[9],
                place_of_birth=row[10],
                charges=row[11],
                wanted_by=row[12],
                status=row[13],
                publication=row[14],
                last_modified=row[15],
                reward=row[16],
                details=row[17],
                caution=row[18],
                remarks=row[19],
                images=row[20],
                link=row[21],
            )
            profile.save()

save_to_database()
print('csv saved to db')
