import requests
import json
import pandas as pd
import httpx
from selectolax.parser import HTMLParser





def toronto_fugitive_profiles():
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

def toronto_fugitive_profile_extract():
    """
    Extract data from records.
    """
    profile_links = toronto_fugitive_profiles()
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
        # 'age_min': fbi_data_pd['items'][i]['age_min'],
        # 'age_max': fbi_data_pd['items'][i]['age_max'],
        # 'height_min': fbi_data_pd['items'][i]['height_min'],
        # 'height_max': fbi_data_pd['items'][i]['height_max'],
        # 'weight': fbi_data_pd['items'][i]['weight'],
        # 'eyes': fbi_data_pd['items'][i]['eyes'],
        # 'hair': fbi_data_pd['items'][i]['hair'],
        # 'distinguishing_marks': fbi_data_pd['items'][i]['scars_and_marks'],
        # 'nationality': fbi_data_pd['items'][i]['nationality'],
        # 'age_range': fbi_data_pd['items'][i]['age_range'],
        # 'date_of_birth': fbi_data_pd['items'][i]['dates_of_birth_used'],
        # 'place_of_birth': fbi_data_pd['items'][i]['place_of_birth'],
        # 'charges': fbi_data_pd['items'][i]['subjects'],
        # 'wanted_by': 'FBI',
        # 'publication': fbi_data_pd['items'][i]['publication'],
        # 'last_modified': fbi_data_pd['items'][i]['modified'],
        # 'status': fbi_data_pd['items'][i]['status'],
        # 'reward': fbi_data_pd['items'][i]['reward_max'],
        # 'details': fbi_data_pd['items'][i]['details'],
        # 'caution': fbi_data_pd['items'][i]['caution'],
        # 'warning': fbi_data_pd['items'][i]['warning_message'],
        # 'images': '',
        # 'link': fbi_data_pd['items'][i]['url'],



class Scraper:
    def __init__(self):
        pass

    def rcmp_fugitive_profiles(self):
        fugitive_profiles = set()
        URL = 'https://www.rcmp-grc.gc.ca/en/wanted'
        response = httpx.get(URL)
        html = HTMLParser(response.text)

        profile_link = html.css('a.text-neutral')
        for link in profile_link:
            fugitive_profiles.add(link.attributes['href'])
        return fugitive_profiles

    def rcmp_fugitive_profile_extractor(self):
        profile_extracts = []
        fugitive_profiles = self.rcmp_fugitive_profiles()
        for profile in fugitive_profiles:
            URL = f'https://www.rcmp-grc.gc.ca/en/{profile}'
            print(URL)
            response = httpx.get(URL)
            html = HTMLParser(response.text)

            # Extracts
            name = html.css('h1.page-header')
            # sex = personal_details[1].text()
            status = html.css_first('p.mrgn-bttm-md').text()
            charges = html.css('ul.list-group li.list-group-item') # list of charges
            last_modified = html.css_first('time')
            description = html.css('div.col-md-9 p') # description[1].text()
            image = html.css_first('img.img-responsive').attributes['src']
            image = 'https://www.rcmp-grc.gc.ca' + image
            link = URL


            # To determine the value associtaed with the extracted list, split the sentence into
            # words, and assign the value to the right variable with the first word
            personal_details = html.css('ul.list-unstyled li')
            alias = ''
            sex = ''
            date_of_birth = ''
            place_of_birth = ''
            eyes = ''
            hair = ''
            height = ''
            weight = ''
            scars = ''
            for detail_list in personal_details:
                details = detail_list.text().split()
                if details[0] == 'Aliases:':
                    alias = details[1:]
                elif details[0] == 'Sex:':
                    sex = details[1:]
                elif details[0] == 'Born:':
                    date_of_birth = details[1:]
                elif details[0] == 'Place':
                    place_of_birth = details[1:]
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
                else:
                    print('nononono')

            # restructure sentence
            profile_values = [alias, sex, date_of_birth, place_of_birth, eyes, hair, height, weight, scars]
            profile_values = [ ''.join(text) if index == 6 or index == 7 else ' '.join(text) for index, text in enumerate(profile_values) ]

            for i in profile_values:
                print(i)

            # for i, val in enumerate(personal_details):
            #     print(f'{i} | {val.text()}')
            # profile = {
            #     'name': html.css('h1.page-header').text(),
            #     'alias': '',
            #     'sex': personal_details[1].text(),
            #     'age_min': '',
            #     'age_max': '',
            #     'height_min': '',
            #     'height_max': '',
            #     'height': '',
            #     'weight': '',
            #     'eyes': '',
            #     'hair': '',
            #     'distinguishing_marks': '',
            #     'nationality': '',
            #     'age_range': '',
            #     'date_of_birth': '',
            #     'place_of_birth': '',
            #     'charges': html.css('ul.list-group li.list-group-item'),
            #     'wanted_by': 'RCMP',
            #     'publication': '',
            #     'last_modified': html.css('time').text(),
            #     'status': html.css_first('p.mrgn-bttm-md').text(),
            #     'reward': '',
            #     'details': description[1].text(),
            #     'caution': '',
            #     'warning': '',
            #     'images': image,
            #     'link': URL,
            # }
            # profile_extracts.append(profile)
            # print(profile)

            print('########################')



def main():
    # toronto_fugitive_profile_extract()
    sc = Scraper()
    sc.rcmp_fugitive_profile_extractor()


if __name__ == '__main__':
    main()
