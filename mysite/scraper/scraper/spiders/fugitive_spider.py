from pathlib import Path

import scrapy


class FugitiveSpider(scrapy.Spider):
    name = "fugitive_spider"
    page_num = 0

    def start_requests(self):
        start_urls = [
            'https://www.fbi.gov/wanted/topten',
        ]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_fugitive_records)

    def parse_fugitive_records(self, response):
        # first_record_on_page = response.meta['first_record_on_page']
        records = response.css('li')
        num_records_returned = len(records)
        print('#######################')
        print(f'<< INFO >> # of fugitive records: {num_records_returned}')

        firstname = response.css('h1::text').get(default='')
        lastname = response.css('').get(default='')
        aliases = response.css('.wanted-person-aliases p::text').get(default='')
        sex = response.css('').get(default='')
        height = response.css('//*[@id="content-core"]/div/div/div[7]/table[1]/tbody/tr[5]/td[1]').get(default='')
        weight = response.css('').get(default='')
        nationality = respones.css('').get(default='')
        date_of_birth = response.css('').get(default='')
        place_of_birth = response.css('').get(default='')
        charges = response.css('.wanted-personwrapper p::text').get(default='')
        wanted_by = response.css('').get(default='')
        date_posted = response.css('').get(default='')
        reward = response.css('.wanted-person-reward p::text').get(default='')
        details = response.css('.wanted-person-caution p::text').get(default='')
        remarks = response.css('.wanted-perons-remarks p::text').get(default='')
        images = response.css('').get(default='')
        wanted_poster_pdf = response.css('').get(default='')


        records = []
        record = {
            'firstname': firstname,
            'lastname': lastname,
            'aliases': aliases,
            'sex': sex,
            'height': height,
            'weight': weight,
            'nationality': nationality,
            'date_of_birth': date_of_birth,
            'place_of_birth': place_of_birth,
            'charges': charges,
            'wanted_by': wanted_by,
            'date_posted': date_posted,
            'reward': reward,
            'details': details,
            'remarks': remarks,
            'images': fugitive_image,
            'wanted_poster_pdf': wanted_poster_pdf
        }
        records.append(record)

        print()

        ########### Request next page ###########
        if num_records_returned > 0:
            self.page_num += 1
            first_record_on_page = int(first_record_on_page) + 25
            next_url = ''
            yield scrapy.Request(url=url, callback=self.parse_fugitive_records, meta={'first_record_on_page': first_record_on_page})
