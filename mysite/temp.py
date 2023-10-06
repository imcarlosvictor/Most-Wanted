import requests
import json
import pandas as pd
import httpx
from selectolax.parser import HTMLParser






def get_html(page_num: int):
    url = f'https://www.tps.ca/organizational-chart/specialized-operations-command/detective-operations/investigative-services/homicide/most-wanted/?page={page_num}'
    response = httpx.get(url)
    return HTMLParser(response.text)


get_html(1)
