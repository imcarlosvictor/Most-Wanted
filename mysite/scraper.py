import os
import json
import csv
import pandas as pd
import httpx
import requests
from selectolax.parser import HTMLParser


DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
RAW_PROFILE_EXTRACT_CSV = os.path.abspath(os.path.join(DIRECTORY_PATH, './raw_profile_extracts.csv'))


class RcmpScraper:
    def save_to_csv(self, profile_data):
        with open(RAW_PROFILE_EXTRACT_CSV, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(profile_data)
    
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
            print(f'Extracting {current_profile_count} of {len(fugitive_profiles)}')
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
                details = detail_list.text().split()
                if details[0] == 'Aliases:':
                    alias = details[1:]
                elif details[0] == 'Sex:':
                    sex = details[1:]
                elif details[0] == 'Born:':
                    date_of_birth = details[1:]
                elif details[0] == 'Place':
                    place_of_birth = details[3:]
                elif details[0] == 'Eye':
                    eyes = details[2:]
                elif details[0] == 'Hair':
                    hair = details[2:]
                elif details[0] == 'Height:':
                    height = details[1:]
                elif details[0] == 'Weight:':
                    weight = details[1:]
                elif details[0] == 'Tattoos:':
                    pass
                elif details[0] == 'Scars:':
                    scars = details[1:]
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

            # Save profile
            self.save_to_csv(profile_values)
            current_profile_count += 1

            # profile = {
            #     'name': name.text(),
            #     'alias': profile_values[0],
            #     'sex': profile_values[1],
            #     'height': profile_values[6],
            #     'weight': profile_values[7],
            #     'eyes': profile_values[4],
            #     'hair': profile_values[5],
            #     'distinguishing_marks': '',
            #     'nationality': '',
            #     'date_of_birth': profile_values[2],
            #     'place_of_birth': profile_values[3],
            #     'charges': [ charge.text() for charge in charges ],
            #     'wanted_by': 'RCMP',
            #     'status': status,
            #     'publication': '',
            #     'last_modified': last_modified.text(),
            #     'reward': '',
            #     'details': details_cleaned,
            #     'caution': '',
            #     'remarks': '',
            #     'images': image,
            #     'link': URL,
            # }
            # fugitive_profile_extracts.append(profile)

        # for profile in fugitive_profile_extracts:
            # self.raw_data_list.append(list(profile.values()))




class FbiScraper:
    def save_to_csv(self, profile_data):
        with open(RAW_PROFILE_EXTRACT_CSV, 'a', newline='') as file:
            writer = csv.writer(file)
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
            print(f'Extracting {current_profile_count} of {len(fugitive_id_url)}')
            interpol_response = requests.get(url)
            interpol_data = json.loads(interpol_response.content)
            # Check if a profile consists of images
            profile_image = ''
            profile_link = ''
            if interpol_data['_links']:
                if interpol_data['_links']['images']:
                    images = interpol_data['_links']['images']['href'] if interpol_data['_links']['images']['href'] else ''
                if interpol_data['_links']['self']:
                    link = interpol_data['_links']['self']['href'] if interpol_data['_links']['self']['href'] else ''

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
            print(profile_values)

            # Save profile
            # print(profile_values)
            self.save_to_csv(profile_values)
            current_profile_count += 1

    def clean_data(self, profile_val):
        # --------------- SEX ---------------
        if profile_val[2] == 'M':            
            profile_val[2] = 'Male' 
        elif profile_val[2] == 'F':
            profile_val[2] = 'Female'

        # --------------- HEIGHT ---------------
        # Add and extra 0 if necessary and unit of measurement (cm)
        if profile_val[3]:
            height = str(profile_val[3]).replace('.','')
            if len(height) == 2:
                height += '0cm'
            elif len(height) > 2:
                height += 'cm'
            profile_val[3] = height

        # Add unit of measurement
        # --------------- WEIGHT ---------------
        if profile_val[4]:
            weight = str(profile_val[4])
            profile_val[4] = weight + 'kg'

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

        # --------------- PLACE OF BIRTH ---------------
        from deep_translator import GoogleTranslator
        value_to_translate = profile_val[10]
        profile_val[10] = GoogleTranslator(source='auto', target='english').translate(value_to_translate)

        # --------------- CHARGES ---------------
        value_to_translate = profile_val[11]
        profile_val[11] = GoogleTranslator(source='auto', target='english').translate(value_to_translate)

    def save_to_csv(self, profile_data):
        with open(RAW_PROFILE_EXTRACT_CSV, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(profile_data)

            # record = {
            #     'name': firstname + ' ' + lastname,
            #     'alias': '',
            #     'sex': [ interpol_data['sex_id'] if interpol_data['sex_id'] else '' ],
            #     'height': [ interpol_data['height'] if interpol_data['height'] else '' ],
            #     'weight': [ interpol_data['weight'] if interpol_data['weight'] else '' ],
            #     'eyes': [ interpol_data['eyes_colors_id'] if interpol_data['eyes_colors_id'] else '' ],
            #     'hair': [ interpol_data['hairs_id'] if interpol_data['hairs_id'] else '' ],
            #     'distinguishing_marks': [ interpol_data['distinguishing_marks'] if interpol_data['distinguishing_marks'] else '' ],
            #     'nationality': [ interpol_data['nationalities'] if interpol_data['nationalities'] else '' ],
            #     'date_of_birth': [ interpol_data['date_of_birth'] if interpol_data['date_of_birth'] else '' ],
            #     'place_of_birth': [ interpol_data['place_of_birth'] if interpol_data['place_of_birth'] else '' ],
            #     'charges' : [ interpol_data['arrest_warrants'][0]['charge'] if interpol_data['arrest_warrants'][0]['charge'] else '' ],
            #     'wanted_by': [ interpol_data['arrest_warrants'][0]['issuing_country_id'] if interpol_data['arrest_warrants'][0]['issuing_country_id'] else '' ],
            #     'status': 'wanted',
            #     'publication': '',
            #     'last_modified': '',
            #     'reward': '',
            #     'details': '',
            #     'caution': '',
            #     'remarks': '',
            #     'images': images,
            #     'thumbnail': '',
            #     'link': link,
            # }
            # fugitive_profile_extracts.append(record)

        # for profile in fugitive_profiles_extract:
            # self.raw_data_list.append(list(profile.values()))


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

            # #######################################################
            # 'name'
            # 'aliases': fbi_data_pd['items'][i]['aliases'],
            # 'sex': fbi_data_pd['items'][i]['sex'],
            # 'weight': fbi_data_pd['items'][i]['weight'],
            # 'eyes': fbi_data_pd['items'][i]['eyes'],
            # 'hair': fbi_data_pd['items'][i]['hair'],
            # 'distinguishing_marks': fbi_data_pd['items'][i]['scars_and_marks'],
            # 'nationality': fbi_data_pd['items'][i]['nationality'],
            # 'date_of_birth': fbi_data_pd['items'][i]['dates_of_birth_used'],
            # 'place_of_birth': fbi_data_pd['items'][i]['place_of_birth'],
            # 'charges': fbi_data_pd['items'][i]['subjects'],
            # 'wanted_by': 'FBI',
            # 'status': fbi_data_pd['items'][i]['status'],
            # 'publication': fbi_data_pd['items'][i]['publication'],
            # 'last_modified': fbi_data_pd['items'][i]['modified'],
            # 'reward': fbi_data_pd['items'][i]['reward_max'],
            # 'details': fbi_data_pd['items'][i]['details'],
            # 'caution': fbi_data_pd['items'][i]['caution'],
            # 'warning': fbi_data_pd['items'][i]['warning_message'],
            # 'images': '',
            # 'link': fbi_data_pd['items'][i]['url'],




def main():
    rcmp = RcmpScraper()
    fbi = FbiScraper()
    interpol = InterpolScraper()

    # interpol.get_profiles()
    interpol.extract_profile_data()


if __name__ == '__main__':
    main()
