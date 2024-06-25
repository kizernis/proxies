import json
import re
import requests
from bs4 import BeautifulSoup
import concurrent.futures

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
proxies = []

def scrape_proxies_source(proxies_source):
    session = requests.Session()
    session.headers = { 'User-Agent': USER_AGENT }
    if proxies_source == 'spys.me':
        lines = session.get('https://spys.me/proxy.txt').text.splitlines()[6:-2]
        for line in lines:
            proxy, info, *_ = line.split()
            if '-A' not in info and '-H' not in info:
                continue
            proxies.append(proxy)
    else:
        for row in BeautifulSoup(session.get(proxies_source).text, 'lxml').find('section', id='list').tbody.find_all('tr'):
            fields = row.find_all('td')
            if not re.search('elite|anonymous', fields[4].text):
                continue
            proxy = fields[0].text + ':' + fields[1].text
            proxies.append(proxy)

proxies_sources = ('spys.me', 'https://www.sslproxies.org/', 'https://www.google-proxy.net/', 'https://free-proxy-list.net/', 'https://www.us-proxy.org/', 'https://free-proxy-list.net/uk-proxy.html', 'https://free-proxy-list.net/anonymous-proxy.html')
with concurrent.futures.ThreadPoolExecutor(max_workers=len(proxies_sources)) as executor:
    executor.map(scrape_proxies_source, proxies_sources)
proxies = list(dict.fromkeys(proxies))

print(json.dumps(proxies))
