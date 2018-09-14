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
        entry_type = 'experiments'
        super(Exp, self).__init__(exp, entry_type)
        self.assay = self.json['assay_term_name']
        self.attr.update({'assay': 'Assay'})
        if parse:
            self._parse_exp_json()

    def _parse_exp_json(self):
        # experiment info
        self.description = self.json['description']
        # biosample info
        self.biosample = self.json['biosample_summary']
        self.biosample_type = self.json['biosample_type']
        self.biosample_id = self.json['biosample_term_id']
        # target
        if 'target' in self.json:
            self.target = self.json['target']['label']
            self.attr.update({'target': 'Target'})
        # update available attributes
        self.attr.update({'description': 'Description',
                          'biosample': 'Biosample',
                          'biosample_type': 'Biosample Type',
                          'biosample_id': 'Biosample ID'})
