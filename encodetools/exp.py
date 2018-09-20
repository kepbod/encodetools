'''
ENCODE experiment classes
https://www.encodeproject.org/profiles/experiment.json
'''

from .metadata import Entry

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'


class Exp(Entry):
    '''
    ENCODE experiment entry
    '''

    def __init__(self, exp, parse=True):
        if exp.startswith('ENCSR'): # in case exp is not an experiment ID
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