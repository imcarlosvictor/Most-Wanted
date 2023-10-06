import requests
import json
import pandas as pd

################################### FBI ###################################
fbi_fugitive_records = []
page_number = 1
def get_fbi_fugitive_records(page: int):
    """
    Implements api pagination.
    """
    response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page': page})
    fbi_data = response.json()
    fbi_data_pd = pd.DataFrame.from_dict(fbi_data)

    # Base case
    if len(fbi_fugitive_records) == fbi_data['total']:
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
            'distinguishing_marks': fbi_data_pd['items'][i]['scars_and_marks'],
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
        fbi_fugitive_records.append(record)

    page_number += 1
    print('#########################')
    # print(page_number)
    print(len(fbi_fugitive_records))
    get_fbi_fugitive_records(page_number)

# get_fbi_fugitive_records(page_number)
# print(fbi_fugitive_records[999])


################################### INTERPOL ###################################
page_num = 1
fugitive_id_urls = []
def interpol_fugitive_id(page, url_list):
    # base case
    if page == 9:
        return

    interpol_response = requests.get(f'https://ws-public.interpol.int/notices/v1/red?page={page}')
    interpol_data = json.loads(interpol_response.content)

    additional_info_url = 'https://ws-public.interpol.int/notices/v1/red/'
    for i in range(0, len(interpol_data['_embedded']['notices'])):
        # interpol_data['_embedded']['notices'][i]['']
        id = interpol_data['_embedded']['notices'][i]['entity_id']
        url = additional_info_url + id.replace('/','-')
        url_list.append(url)

    page += 1
    interpol_fugitive_id(page, url_list)


interpol_fugitive_records = []
def get_interpol_records(individual_red_notice_url):
    # Iterate over URLs of fugitive recrods
    for url in individual_red_notice_url:
        # print(len(interpol_fugitive_records))
        interpol_response = requests.get(url)
        interpol_data = json.loads(interpol_response.content)

        # print(interpol_data['arrest_warrants'])
        print(url)
        # print(interpol_data['_links']['thumbnail'])
        if interpol_data['_links']:
            if interpol_data['_links']['images']:
                images = [ interpol_data['_links']['images']['href'] if interpol_data['_links']['images']['href'] else '' ],
            if interpol_data['_links']['self']:
                link = [ interpol_data['_links']['self']['href'] if interpol_data['_links']['self']['href'] else '' ],

        record = {
            'firstname': [ interpol_data['forename'] if interpol_data['forename'] else '' ],
            'lastname': [ interpol_data['name'] if interpol_data['name'] else '' ],
            'aliases': '',
            'sex': [ interpol_data['sex_id'] if interpol_data['sex_id'] else '' ],
            'age_min': '',
            'age_max': '',
            'height_min': '',
            'height_max': '',
            'height': [ interpol_data['height'] if interpol_data['height'] else '' ],
            'weight': [ interpol_data['weight'] if interpol_data['weight'] else '' ],
            'eyes': [ interpol_data['eyes_colors_id'] if interpol_data['eyes_colors_id'] else '' ],
            'hair': [ interpol_data['hairs_id'] if interpol_data['hairs_id'] else '' ],
            'distinguishing_marks': [ interpol_data['distinguishing_marks'] if interpol_data['distinguishing_marks'] else '' ],
            'nationality': [ interpol_data['nationalities'] if interpol_data['nationalities'] else '' ],
            'age_range': '',
            'date_of_birth': [ interpol_data['date_of_birth'] if interpol_data['date_of_birth'] else '' ],
            'place_of_birth': [ interpol_data['place_of_birth'] if interpol_data['place_of_birth'] else '' ],
            'charges' : [ interpol_data['arrest_warrants'][0]['charge'] if interpol_data['arrest_warrants'][0]['charge'] else '' ],
            'wanted_by': [ interpol_data['arrest_warrants'][0]['issuing_country_id'] if interpol_data['arrest_warrants'][0]['issuing_country_id'] else '' ],
            'publication': '',
            'last_modified': '',
            'status': 'wanted',
            'reward': '',
            'details': '',
            'caution': '',
            'warning': '',
            'images': images,
            'thumbnail': '',
            'link': link,
        }
        interpol_fugitive_records.append(record)

# interpol_fugitive_id(page_num, fugitive_id_urls)
# get_interpol_records(fugitive_id_urls)
print('complete')



from selectolax.parser import HTMLParser

class record_scraper:
    def __init__(self):
        self.interpol_fugitive_records = []
        self.fbi_fugitive_records = []

    def interpol_records(self):
        URL = 'https://www.interpol.int/en/How-we-work/Notices/Red-Notices/View-Red-Notices'
        interpol_response = requests.get(URL)
        interpol_data = json.loads(interpol_response.content)
        # interpol_data_pd = pd.DataFrame(interpol_data)

        # Base case
        if page == 20:
            return





    def fbi_records(self):
        pass

