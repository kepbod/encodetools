'''
ENCODE meta classes
'''

import requests
import requests.compat

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'
__all__ = ['Entry']


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
        self.id = '/%s/%s/' % (etype, eid)
        self.baseurl = 'https://www.encodeproject.org/'
        self.url = requests.compat.urljoin(self.baseurl, self.id)
        # available attributes
        self.attr = {'accession': 'Accession ID',
                     'url': 'URL'}
        # parse json
        if json_d is None:
            self.json = self._fetch_json()  # fetch json form ENCODE
        else:
            self.json = json_d

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
        info = []
        for key in self.__dict__:
            if key in self.attr:
                info.append('{}: {}'.format(self.attr[key],
                                            self.__dict__[key]))
        return '\n'.join(info)

    def __repr__(self):
        return self.__str__()
