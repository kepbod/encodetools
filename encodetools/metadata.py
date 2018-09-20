'''
ENCODE meta classes
'''

import requests
import requests.compat

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'


# use ujson if possible
try:
    import ujson
    requests.models.json = ujson
except ImportError:
    pass


class Entry(object):
    '''
    Meta class of ENCODE entry
    '''

    def __init__(self, eid, etype=None, json_d=None):
        if etype is None:  # in case use meta class directly
            raise Exception('etype should not be None!')
        # basic info
        self.accession = eid
        self._id = '/%s/%s/' % (etype, eid)
        self._baseurl = 'https://www.encodeproject.org/'
        self.url = requests.compat.urljoin(self._baseurl, self._id)
        # available attributes
        self._attr = {'accession': 'Accession ID',
                     'url': 'URL'}
        # parse json
        if json_d is None:
            self._json = self._fetch_json()  # fetch json form ENCODE
        else:
            self._json = json_d

    def _fetch_json(self):
        '''
        Fetch json file from ENCODE
        '''
        headers = {'accept': 'application/json'}
        response = requests.get(self.url, headers=headers)
        return response.json()

    def __str__(self):
        '''
        List all the available infomation
        '''
        return '\n'.join('{}: {}'.format(self._attr[key],
                                         self.__dict__[key])
                         for key in self.__dict__
                         if key in self._attr)

    def __repr__(self):
        return self.__str__()

    @property
    def attributes(self):
        '''
        List all the available attributes
        '''
        print('\n'.join('{}: {}'.format(key, self._attr[key])
                        for key in self._attr))
