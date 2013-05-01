import requests
import BeautifulSoup
import re

BASE_URL = 'http://www.amigoexpress.com'

MAIN_URL = BASE_URL + '/itinerarySearch/QC/rideshares_from_Montreal.html'
APPEND_TO_LOCS = 'Canada'

class Bot(object):
    def __init__(self):
        self.locations = []

    def parse_url(self, url):
        print '{0} locations'.format(len(self.locations))
        print 'parsing {0}'.format(url)
        user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'}
        cont = requests.get(url, headers=user_agent).content
        soup = BeautifulSoup.BeautifulSoup(cont)
        dests = soup.findAll('div', {'class': 'city destination'})
        locations = []
        for dest in dests:
            dest = dest.find('strong').contents[0]
            self.locations.append(dest)

        next = soup.find('a', {'class': 'Next'})
        if next:
            next = next.get('href')
            self.parse_url(BASE_URL + next)

    def geocode(self, location):
        location += ' {0}'.format(APPEND_TO_LOCS)
        latlon = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false'.format(location)).json()['results'][0]\
                ['geometry']['location']
        return ','.join(map(str, [latlon['lat'], latlon['lng']]))

    def output_map(self):
        locs = set(self.locations)
        url = 'http://maps.google.com/maps/api/staticmap?zoom=4&size=512x512&sensor=false&maptype=roadmap'
        markers = []
        for loc in locs:
            try:
                loc = loc.encode('utf8')
                markers.append('color:green|label:{0}|{1}'.format(loc, self.geocode(loc)))
            except IndexError:
                continue
        return url + '&'.join(['markers={0}'.format(n) for n in markers])



b = Bot()
b.parse_url(MAIN_URL)
print b.output_map()
