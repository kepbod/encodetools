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
        if not fid.startswith('ENCFF'): # in case fid is not a file ID
            raise Exception('{} is not one file ID!'.format(fid))
        entry_type = 'file'
        super(SeqFile, self).__init__(fid, entry_type, json_d=json_d)
        # experiment info
        self.exp = self._json['dataset'].split('/')[2]
        if assay is not None:
            self.assay = assay
        else:
            self.assay = Exp(self.exp, parse=False).assay
        # file info
        self.file_format = self._json['file_format']
        self.output_type = self._json['output_type']
        self.file_url = requests.compat.urljoin(self._baseurl,
                                                self._json['href'])
        self.file_status = self._json['status']
        self.file_size = self._json['file_size']
        self.file_md5 = self._json['md5sum']
        # update available attributes
        self._attr.update({'exp': 'Experiment',
                           'assay': 'Assay',
                           'file_format': 'File Format',
                           'output_type': 'Output Type',
                           'file_url': 'File URL',
                           'file_status': 'File Status',
                           'file_size': 'File Size',
                           'file_md5': 'File MD5'})


class RawFile(SeqFile):
    '''
    ENCODE raw file entry
    '''

    def __init__(self, fid, json_d=None, assay=None):
        super(RawFile, self).__init__(fid, json_d=json_d, assay=assay)
        self.run_type = self._json['run_type']
        self.read_length = self._json['read_length']
        self.read_count = self._json['read_count']
        self._attr.update({'run_type': 'Run Type',
                           'read_length': 'Read Length',
                           'read_count': 'Read Count'})

class ProcessedFile(SeqFile):
    '''
    ENCODE processed file entry
    '''

    def __init__(self, fid, json_d=None, assay=None):
        super(ProcessedFile, self).__init__(fid, json_d=json_d, assay=assay)
        self.assembly = self._json['assembly']
        self._attr.update({'assembly': 'Assembly'})
