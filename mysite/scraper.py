import os
import json
import csv
import httpx
import requests
import pandas as pd
import country_converter as coco
from selectolax.parser import HTMLParser
from deep_translator import GoogleTranslator


DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
RAW_PROFILE_EXTRACT_CSV = os.path.abspath(os.path.join(DIRECTORY_PATH, './data_extracts/raw_profile_extracts.csv'))


class RcmpScraper:
    def get_profiles(self):
        fugitive_profile_links = set()
        URL = 'https://www.rcmp-grc.gc.ca/en/wanted'
        response = httpx.get(URL)
        html = HTMLParser(response.text)

        profile_link = html.css('a.text-neutral')
        for link in profile_link:
            fugitive_profile_links.add(link.attributes['href'])

        return fugitive_profile_links

    def extract_profile_data(self):
        print('------------------------------------')
        print('Extracting RCMP Fugitives...')
        print('------------------------------------')
        fugitive_profile_extracts = []
        fugitive_profiles = self.get_profiles()
        current_profile_count = 1
        for profile in fugitive_profiles:
            print(f'Extracting {current_profile_count} of {len(fugitive_profiles)} RCMP Profiles')
            URL = f'https://www.rcmp-grc.gc.ca/en/{profile}'
            # print(URL)
            response = httpx.get(URL)
            html = HTMLParser(response.text)

            # Extracts
            name = html.css_first('h1.page-header').text()
            alias = ''
            sex = ''
            height = ''
            weight = ''
            eyes = ''
            hair = ''
            distinguishing_marks = ''
            nationality = ''
            date_of_birth = ''
            place_of_birth = ''
            charges = html.css('ul.list-group li.list-group-item') # list of charges
            charges = [ charge.text() for charge in charges ]
            wanted_by = 'rcmp'
            status = 'wanted'
            publication = ''
            last_modified = html.css_first('time').text()
            reward = ''
            details = html.css('div.col-md-9 p') # description[1].text()
            details = details[1].text()
            details_cleaned = details.replace('\xa0', ' ')
            caution = ''
            remarks = ''
            image = html.css_first('img.img-responsive').attributes['src']
            image = 'https://www.rcmp-grc.gc.ca' + image
            link = URL
            # To determine the value associtaed with the extracted list, split the sentence into
            # words, and assign the value to the right variable with the first word
            personal_details = html.css('ul.list-unstyled li')
            for detail_list in personal_details:
                description_list = detail_list.text().split()
                if description_list[0] == 'Aliases:':
                    alias = description_list[1:]
                elif description_list[0] == 'Sex:':
                    sex = description_list[1:]
                elif description_list[0] == 'Born:':
                    date_of_birth = description_list[1:]
                elif description_list[0] == 'Place':
                    place_of_birth = description_list[3:]
                elif description_list[0] == 'Eye':
                    eyes = description_list[2:]
                elif description_list[0] == 'Hair':
                    hair = description_list[2:]
                elif description_list[0] == 'Height:':
                    height = description_list[1:]
                elif description_list[0] == 'Weight:':
                    weight = description_list[1:]
                elif description_list[0] == 'Tattoos:':
                    pass
                elif description_list[0] == 'Scars:':
                    scars = description_list[1:]
            profile_values = [
                name,
                alias,
                sex,
                height,
                weight,
                eyes,
                hair,
                distinguishing_marks,
                nationality,
                date_of_birth,
                place_of_birth,
                charges,
                wanted_by,
                status,
                publication,
                last_modified,
                reward,
                details,
                caution,
                remarks,
                image,
                link,
            ]
            # Restructure sentence for height and weight
            profile_values = [ ''.join(text) for text in profile_values ]
            # Clean alias values
            profile_values[1] = profile_values[1].replace('/', ' / ')
            profile_values[1] = profile_values[1].replace(',', ', ')
            profile_values_clean = ''
            for text in profile_values[1]:
                if text.isupper():
                    profile_values_clean = profile_values_clean + ' ' + text.capitalize()
                else:
                    profile_values_clean += text
            profile_values[1] = profile_values_clean 

            # Clean data
            self.clean_data(profile_values)

            # Save profile
            self.save_to_csv(profile_values)
            current_profile_count += 1

    def clean_data(self, profile_val):
        # --------------- HEIGHT ---------------
        height_in_cm_reversed  = profile_val[3][-1:-6:-1]
        profile_val[3] = height_in_cm_reversed[-1:1:-1]
        if profile_val[3] != '':
            profile_val[3] = int(profile_val[3]) # INT field
        else:
            profile_val[3] = 0

        # --------------- WEIGHT ---------------
        profile_val[4] = profile_val[4][7:-2]
        if profile_val[4] != '':
            profile_val[4] = int(profile_val[4]) # INT field
        else:
            profile_val[4] = 0

        # --------------- DATE OF BIRTH ---------------
        pos = len(profile_val[9]) - 4
        new_date_value = profile_val[9][:pos] + ' ' + profile_val[9][pos:]
        profile_val[9] = new_date_value

        for i in range(0, len(profile_val) - 2):
            if type(profile_val[i]) == str:
                profile_val[i] = profile_val[i].lower()

    def save_to_csv(self, profile_data):
        with open(RAW_PROFILE_EXTRACT_CSV, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(profile_data)


class FbiScraper:
    def save_to_csv(self, profile_data):
        with open(RAW_PROFILE_EXTRACT_CSV, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(profile_data)

    def extract_profile_data(self):
        """
        Implements api pagination.
        """
        print('------------------------------------')
        print('Extracting FBI Fugitives...')
        print('------------------------------------')
        fugitive_profile_extracts = []
        page = 1
        while True:
            response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page': page})
            print(response)
            fbi_data = response.json()
            # fbi_data = json.loads(response.content)
            fbi_data_pd = pd.DataFrame.from_dict(fbi_data)

            # Base case
            if len(fugitive_profile_extracts) == fbi_data['total']:
                break

            for i in range(0, len(fbi_data_pd['items'])):
                age = ''
                if fbi_data_pd['items'][i]['age_min']:
                    age = str(fbi_data_pd['items'][i]['age_min']) + '-' + str(fbi_data_pd['items'][i]['age_max'])
                else:
                    age = str(fbi_data_pd['items'][i]['age_max'])

                height = ''
                if fbi_data_pd['items'][i]['height_min']:
                    height = str(fbi_data_pd['items'][i]['height_min']) + '-' + str(fbi_data_pd['items'][i]['height_max'])
                else:
                    height = str(fbi_data_pd['items'][i]['height_max'])
                profile = {
                    'name': fbi_data_pd['items'][i]['title'],
                    'alias': fbi_data_pd['items'][i]['aliases'],
                    'sex': fbi_data_pd['items'][i]['sex'],
                    'height': '',
                    'weight': fbi_data_pd['items'][i]['weight'],
                    'eyes': fbi_data_pd['items'][i]['eyes'],
                    'hair': fbi_data_pd['items'][i]['hair'],
                    'distinguishing_marks': fbi_data_pd['items'][i]['scars_and_marks'],
                    'nationality': fbi_data_pd['items'][i]['nationality'],
                    'date_of_birth': fbi_data_pd['items'][i]['dates_of_birth_used'],
                    'place_of_birth': fbi_data_pd['items'][i]['place_of_birth'],
                    'charges': fbi_data_pd['items'][i]['subjects'],
                    'wanted_by': 'FBI',
                    'status': fbi_data_pd['items'][i]['status'],
                    'publication': fbi_data_pd['items'][i]['publication'],
                    'last_modified': fbi_data_pd['items'][i]['modified'],
                    'reward': fbi_data_pd['items'][i]['reward_max'],
                    'details': fbi_data_pd['items'][i]['details'],
                    'caution': fbi_data_pd['items'][i]['caution'],
                    'remarks': fbi_data_pd['items'][i]['warning_message'],
                    'images': '',
                    'link': fbi_data_pd['items'][i]['url'],
                }
                fugitive_profile_extracts.append(profile)
                # print(profile)
            page += 1

        for profile in fugitive_profile_extracts:
            self.raw_data_list.append(list(profile.values()))


class InterpolScraper:
    def get_profiles(self):
        fugitive_id_list = []
        for i in range(0, 346):
            interpol_response = requests.get(f'https://ws-public.interpol.int/notices/v1/red?page={i}')
            interpol_data = json.loads(interpol_response.content)

            # Base case
            if interpol_data['query']['page'] != i:
                return fugitive_id_list

            additional_info_url = 'https://ws-public.interpol.int/notices/v1/red/'
            for i in range(0, len(interpol_data['_embedded']['notices'])):
                entity_id = interpol_data['_embedded']['notices'][i]['entity_id']
                fugitive_id = additional_info_url + entity_id.replace('/','-')
                fugitive_id_list.append(fugitive_id)

        return fugitive_id_list

    def extract_profile_data(self):
        print('------------------------------------')
        print('Extracting Interpol Fugitives...')
        print('------------------------------------')
        # fugitive_profile_extracts = []
        fugitive_id_url = self.get_profiles()
        current_profile_count = 1
        for url in fugitive_id_url:
            print(f'Extracting {current_profile_count} of {len(fugitive_id_url)} Interpol Profiles')
            interpol_response = requests.get(url)
            interpol_data = json.loads(interpol_response.content)
            # Check if a profile consists of images
            try:
                profile_image = ''
                if interpol_data['_links']:
                    if interpol_data['_links']['images']:
                        profile_image = interpol_data['_links']['thumbnail']['href'] if interpol_data['_links']['thumbnail']['href'] else ''
            except:
                print('No image')

            firstname = interpol_data['forename'] if interpol_data['forename'] else ''
            lastname = interpol_data['name'] if interpol_data['name'] else ''

            # Extracts
            name = firstname + ' ' + lastname
            alias = ''
            sex = interpol_data['sex_id'] if interpol_data['sex_id'] else ''
            height = interpol_data['height'] if interpol_data['height'] else ''
            weight = interpol_data['weight'] if interpol_data['weight'] else ''
            eyes = interpol_data['eyes_colors_id'] if interpol_data['eyes_colors_id'] else ''
            hair = interpol_data['hairs_id'] if interpol_data['hairs_id'] else ''
            distinguishing_marks = interpol_data['distinguishing_marks'] if interpol_data['distinguishing_marks'] else ''
            nationality = interpol_data['nationalities'] if interpol_data['nationalities'] else ''
            date_of_birth = interpol_data['date_of_birth'] if interpol_data['date_of_birth'] else ''
            place_of_birth = interpol_data['place_of_birth'] if interpol_data['place_of_birth'] else ''
            charges = interpol_data['arrest_warrants'][0]['charge'] if interpol_data['arrest_warrants'][0]['charge'] else ''
            wanted_by = interpol_data['arrest_warrants'][0]['issuing_country_id'] if interpol_data['arrest_warrants'][0]['issuing_country_id'] else ''
            status = 'wanted'
            publication = ''
            last_modified = ''
            reward = ''
            details = ''
            caution = ''
            remarks = ''
            image = profile_image
            link = ''

            profile_values = [
                name,
                alias,
                sex,
                height,
                weight,
                eyes,
                hair,
                distinguishing_marks,
                nationality,
                date_of_birth,
                place_of_birth,
                charges,
                wanted_by,
                status,
                publication,
                last_modified,
                reward,
                details,
                caution,
                remarks,
                image,
                link,
            ]

            # Clean data
            self.clean_data(profile_values)

            # Save profile
            self.save_to_csv(profile_values)
            current_profile_count += 1

    def clean_data(self, profile_val):
        # --------------- SEX ---------------
        if profile_val[2] == 'M':            
            profile_val[2] = 'Male' 
        elif profile_val[2] == 'F':
            profile_val[2] = 'Female'

        # --------------- HEIGHT ---------------
        if profile_val[3]:
            height = str(profile_val[3]).replace('.','')
            if len(height) == 2:
                height += '0'
        # Convert to INT
        if profile_val[3] != '':
            profile_val[3] = int(height)
        else:
            profile_val[3] = 0

        # --------------- WEIGHT ---------------
        # Convert to INT
        if profile_val[4] != '':
            profile_val[4] = int(profile_val[4])
        else:
            profile_val[4] = 0

        # --------------- EYES ---------------
        if 'BLA' in profile_val[5]:
            profile_val[5] = 'black'
        elif 'BRO' in profile_val[5]:
            profile_val[5] = 'brown'
        elif 'BROH' in profile_val[5]:
            profile_val[5] = 'brown'
        elif 'BROD' in profile_val[5]:
            profile_val[5] = 'brown'
        elif 'BLU' in profile_val[5]:
            profile_val[5] = 'blue'
        else:
            profile_val[5] = ''

        # --------------- HAIR ---------------
        if 'BLA' in profile_val[6]:
            profile_val[6] = 'black'
        elif 'BRO' in profile_val[6]:
            profile_val[6] = 'brown'
        elif 'BROH' in profile_val[6]:
            profile_val[6] = 'brown'
        elif 'BROD' in profile_val[6]:
            profile_val[6] = 'brown'
        elif 'BLU' in profile_val[6]:
            profile_val[6] = 'blue'
        else:
            profile_val[6] = ''

        # --------------- NATIONALITY ---------------
        country_name_list = []
        for country_code in profile_val[8]:
            country = coco.convert(names=country_code, to='name_short')
            country_name_list.append(country)
        profile_val[8] = ', '.join(country_name_list)

        try:
            # --------------- DISTINGUISHING MARKS ---------------
            if profile_val[7]:
                # --------------- PLACE OF BIRTH ---------------
                value_to_translate = profile_val[7]
                profile_val[7] = GoogleTranslator(source='auto', target='english').translate(value_to_translate)

            # --------------- PLACE OF BIRTH ---------------
            if profile_val[10]:
                value_to_translate = profile_val[10]
                profile_val[10] = GoogleTranslator(source='auto', target='english').translate(value_to_translate)

            # --------------- CHARGES ---------------
            if profile_val[11]:
                value_to_translate = profile_val[11]
                profile_val[11] = GoogleTranslator(source='auto', target='english').translate(value_to_translate)
        except:
            print('No description to translate')

        # --------------- WANTED BY ---------------
        countries = profile_val[12].replace('[','')
        countries = countries.replace(']','')
        country_code_list = countries.split(',')

        country_name_list = []
        for country_code in country_code_list:
            country = coco.convert(names=country_code, to='name_short')
            country_name_list.append(country)
        profile_val[12] = ', '.join(country_name_list)

        # Lower case all values
        for i in range(0, len(profile_val) - 2):
            if type(profile_val[i]) == str:
                profile_val[i] = profile_val[i].lower()

    def save_to_csv(self, profile_data):
        with open(RAW_PROFILE_EXTRACT_CSV, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(profile_data)


class TorontoPeelPoliceScraper:
    def get_profiles(self):
        """
        Extract records.
        """
        profile_links = set()
        for i in range(1, 5):
            url = f'https://www.tps.ca/organizational-chart/specialized-operations-command/detective-operations/investigative-services/homicide/most-wanted/?page={i}'
            response = httpx.get(url)
            html = HTMLParser(response.text)

            # Base case
            current_page_number = html.css_first('div.pagination li.active').text()
            if int(current_page_number) != i:
                break

            # Extract fugitive profile links
            links = html.css('article.suspect a')
            for link in links:
                profile_links.add(link.attributes['href'])

        return profile_links

    def extract_profile_data(self):
        """
        Extract data from records.
        """
        profile_links = toronto_fugitive_profiles_list()
        link = list(profile_links)
        url = f'https://www.tps.ca{link[2]}'
        print(url)
        response = httpx.get(url)
        html = HTMLParser(response.text)

        # Extract
        name = html.css_first('div.people-content h1').text()
        print(name)
        info_block = html.css('div.meta p')

        charge = info_block[0].text().strip()
        print(charge)

        profile_content = html.css('div.people-content p')
        # print(profile_content)
        print(profile_content[3].text().strip())
        print(profile_content[4].text().strip())
        # print(profile_content[2].text().strip())
        print('\n')

        for link in profile_links:
            url = f'https://www.tps.ca{link}'
            print(url)
            response = httpx.get(url)
            html = HTMLParser(response.text)

            # Extract
            name = html.css_first('div.people-content h1').text()
            print(name)
            info_block = html.css('div.meta p')

            charge = info_block[0].text().strip()
            print(charge)

            profile_content = html.css('div.people-content p')
            # print(profile_content)
            print(profile_content[3].text().strip())
            # print(profile_content[3].text().strip())
            # print(profile_content[2].text().strip())
            print('\n')



def main():

    csv_header_list = [
        'Name',
        'Alias',
        'Sex',
        'Height (cm)',
        'Weight (kg)',
        'Eyes',
        'Hair',
        'Distinguishing Marks',
        'Nationality',
        'Date of Birth',
        'Place of Birth',
        'Charges',
        'Wanted By',
        'Status',
        'Publication',
        'Last Modified',
        'Reward',
        'Details',
        'Caution',
        'Remarks',
        'Images',
        'Link',
    ]

    # open CSV and assign headers
    with open(RAW_PROFILE_EXTRACT_CSV, 'w') as file:
        dw = csv.DictWriter(file, delimiter=',', fieldnames=csv_header_list)
        dw.writeheader()

    # create scrapers
    rcmp = RcmpScraper()
    fbi = FbiScraper()
    interpol = InterpolScraper()

    rcmp.extract_profile_data()
    interpol.extract_profile_data()


if __name__ == '__main__':
    main()
