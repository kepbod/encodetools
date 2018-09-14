'''
ENCODE file classes
https://www.encodeproject.org/profiles/file.json
'''

import requests.compat
from .metadata import Entry
from .exp import Exp

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'


class SeqFile(Entry):
    '''
    Meta class of ENCODE file entry
    '''

    def __init__(self, fid, json_d=None, assay=None):
        entry_type = 'file'
        super(SeqFile, self).__init__(fid, entry_type, json_d=json_d)
        # experiment info
        self.exp = self.json['dataset'].split('/')[2]
        if assay is not None:
            self.assay = assay
        else:
            self.assay = Exp(self.exp, parse=False).assay
        # file info
        self.file_format = self.json['file_format']
        self.output_type = self.json['output_type']
        self.file_md5 = self.json['md5sum']
        self.file_url = requests.compat.urljoin(self.baseurl,
                                                self.json['href'])
        # update available attributes
        self.attr.update({'exp': 'Experiment',
                          'assay': 'Assay',
                          'file_format': 'File Format',
                          'output_type': 'Output Type',
                          'file_url': 'File URL',
                          'file_md5': 'File MD5'})