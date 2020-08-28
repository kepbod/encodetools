'''
ENCODE experiment classes
https://www.encodeproject.org/profiles/experiment.json
'''

import sys
from .metadata import Entry
from .expfile import RawFile, ProcessedFile

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'
__all__ = ['Exp']


class Exp(Entry):
    '''
    ENCODE experiment entry
    '''

    def __init__(self, exp, parse=True):
        if not exp.startswith('ENCSR'):  # in case exp is not an experiment ID
            raise Exception('{} is not one experiment ID!'.format(exp))
        entry_type = 'experiments'
        super(Exp, self).__init__(exp, entry_type)
        # assay info
        self.assay = self._json['assay_term_name']
        self._attr.update({'assay': 'Assay'})
        if parse:
            self._parse_exp_json()

    def _parse_exp_json(self):
        # experiment info
        self.description = self._json['description']
        # biosample info
        self.biosample = self._json['biosample_summary']
        self.biosample_type = self._json['biosample_type']
        self.biosample_id = self._json['biosample_term_id']
        # target
        if 'target' in self._json:
            self.target = self._json['target']['label']
            self._attr.update({'target': 'Target'})
        # update available attributes
        self._attr.update({'description': 'Description',
                           'biosample': 'Biosample',
                           'biosample_type': 'Biosample Type',
                           'biosample_id': 'Biosample ID'})

    def fetch_file(self, process_type='all', file_type=None):
        file_json = self._json['files']
        for f in file_json:
            fid = f['accession']
            if file_type is not None:
                if isinstance(file_type, list):
                    if f['file_type'] in file_type:
                        if f['file_type'] == 'fastq':
                            yield RawFile(fid, json_d=f, assay=self.assay)
                        else:
                            yield ProcessedFile(fid, json_d=f,
                                                assay=self.assay)
                elif file_type == f['file_type']:
                    if f['file_type'] == 'fastq':
                        yield RawFile(fid, json_d=f, assay=self.assay)
                    else:
                        yield ProcessedFile(fid, json_d=f, assay=self.assay)
            elif process_type in ['all', 'raw', 'processed']:
                if f['output_category'] == 'raw data':
                    is_raw = True
                else:
                    is_raw = False
                if process_type == 'raw':
                    if is_raw:
                        yield RawFile(fid, json_d=f, assay=self.assay)
                elif process_type == 'processed':
                    if not is_raw:
                        yield ProcessedFile(fid, json_d=f, assay=self.assay)
                else:
                    if is_raw:
                        yield RawFile(fid, json_d=f, assay=self.assay)
                    else:
                        yield ProcessedFile(fid, json_d=f, assay=self.assay)
            else:
                sys.exit('If you did not assign file_type, ' +
                         'process_type should be "all", "raw" or "processed"')

    def fetch_control(self):
        controls = self._json['possible_controls']
        if controls:
            return [ctrl['accession'] for ctrl in controls]
        else:
            return None
