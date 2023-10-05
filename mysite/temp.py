import requests
import json
import pandas as pd

################################### FBI
fbi_records = []
page_number = 1
def get_fbi_records(page_number: int):
    """
    Implements api pagination.
    """
    response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page': page_number})
    fbi_data = response.json()
    fbi_data_pd = pd.DataFrame.from_dict(fbi_data)

    # Base case
    if len(fbi_records) == fbi_data['total']:
        return

    for i in range(0, len(fbi_data_pd['items'])):
        record = {
            'name': fbi_data_pd['items'][i]['title'],
            'aliases': fbi_data_pd['items'][i]['aliases'],
            'sex': fbi_data_pd['items'][i]['sex'],
            'age_min': fbi_data_pd['items'][i]['age_min'],
            'age_max': fbi_data_pd['items'][i]['age_max'],
            'height_min': fbi_data_pd['items'][i]['height_min'],
            'height_max': fbi_data_pd['items'][i]['height_max'],
            'weight': fbi_data_pd['items'][i]['weight'],
            'eyes': fbi_data_pd['items'][i]['eyes'],
            'hair': fbi_data_pd['items'][i]['hair'],
            'unique_features': fbi_data_pd['items'][i]['scars_and_marks'],
            'nationality': fbi_data_pd['items'][i]['nationality'],
            'age_range': fbi_data_pd['items'][i]['age_range'],
            'date_of_birth': fbi_data_pd['items'][i]['dates_of_birth_used'],
            'place_of_birth': fbi_data_pd['items'][i]['place_of_birth'],
            'charges': fbi_data_pd['items'][i]['subjects'],
            'wanted_by': 'FBI',
            'publication': fbi_data_pd['items'][i]['publication'],
            'last_modified': fbi_data_pd['items'][i]['modified'],
            'status': fbi_data_pd['items'][i]['status'],
            'reward': fbi_data_pd['items'][i]['reward_max'],
            'details': fbi_data_pd['items'][i]['details'],
            'caution': fbi_data_pd['items'][i]['caution'],
            'warning': fbi_data_pd['items'][i]['warning_message'],
            'images': '',
            'link': fbi_data_pd['items'][i]['url'],
        }
        fbi_records.append(record)

    page_number += 1
    print('#########################')
    # print(page_number)
    print(len(fbi_records))
    get_fbi_records(page_number)



get_fbi_records(page_number)
print(fbi_records[999])




################################### INTERPOL
# interpol_response = requests.get('https://ws-public.interpol.int/notices/v1/red')
# interpol_data = json.loads(interpol_response.content)

# # print(interpol_data)
# fugitive_ID= []
# for i in range(0, len(interpol_data['_embedded']['notices'])):
#     # interpol_data['_embedded']['notices'][i]['']
#     fugitive_ID.append(interpol_data['_embedded']['notices'][i]['entity_id'])

# fugitive_ID = [ id.replace('/','-') for id in fugitive_ID ]
# print(fugitive_ID)

# item = []
# for i in range(0, len(fugitive_ID)):
#     response = requests.get(f'https://ws-public.interpol.int/notices/v1/red/{fugitive_ID[i]}')
#     data = json.loads(response.content)

#     print(response.status_code)
#     # print(f'https://ws-public.interpol.int/notices/v1/red/{fugitive_ID[i]}')
#     record = {
#         'firstname': data['forename'],
#         'lastname' : data['name'],
#         'aliases' : '',
#         'sex' : data['sex_id'],
#         'height' : data['height'],
#         'weight' : data['weight'],
#         'nationality' : data['nationalities'],
#         'date_of_birth' : data['date_of_birth'],
#         'place_of_birth' : data['place_of_birth'],
#         # 'charges' : data['arrest_warrants'][1]['charge'],
#         'wanted_by' : '',
#         'date_posted' : '',
#         'reward' : '',
#         'details' : '',
#         'remarks' : data['distinguishing_marks'],
#         'images' : '',
#         'wanted_poster_pdf' : '',
#     }
#     item.append(record)

# for record in item:
#     print(record)
#     print('\n')
