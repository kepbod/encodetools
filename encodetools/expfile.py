import requests
from .metadata import Entry
from .utils import fetch_attr


class SeqFile(Entry):
    '''
    Meta class of ENCODE file entry
    '''
    def __init__(self, fid, json_d=None):
        entry_type = 'file'
        super(SeqFile, self).__init__(fid, entry_type, json_d=json_d)
        self._parse_file_json()

    def _parse_file_json(self):
        # experiment info
        self.exp = self.json['dataset']
        # file info
        self.file_type = self.json['file_type']
        self.status = self.json['status']
        self.file_url = requests.compat.urljoin(self.baseurl,
                                                self.json['href'])
        self.file_md5 = self.json['md5sum']
        self.file_size = self.json['file_size']
        if 'replicate' in self.json:
            # replicate info
            replicate = self.json['replicate']
            biorep = 'biological_replicate_number'
            tchrep = 'technical_replicate_number'
            self.biological_replicate = replicate[biorep]
            self.technical_replicate = replicate[tchrep]
            # library info
            if 'library' in self.json['replicate']:
                library = replicate['library']
                fetch_attr(self, LibraryInfo, library, self.attr)
        else:
            # replicate info
            replicate = self.json['technical_replicates'][0].split('_')
            self.biological_replicate = int(replicate[0])
            self.technical_replicate = int(replicate[1])
        # update available attributes
        self.attr.update({'exp': 'Experiment',
                          'file_type': 'File Type',
                          'status': 'Status',
                          'file_url': 'File Download URL',
                          'file_md5': 'File MD5',
                          'file_size': 'File Size',
                          'biological_replicate': 'Biological Replicate',
                          'technical_replicate': 'Technical Replicate'})


class RawFile(SeqFile):
    '''
    ENCODE raw file entry.
    '''
    def __init__(self, fid, json_d=None):
        super(RawFile, self).__init__(fid, json_d=json_d)
        self._parse_rawfile_json()

    def _parse_rawfile_json(self):
        # raw file info
        self.run_type = self.json['run_type']
        self.read_length = self.json['read_length']
        # update available attributes
        self.attr.update({'run_type': 'Run Type',
                          'read_length': 'Read Length'})


class ProcessedFile(SeqFile):
    '''
    ENCODE processed file entry.
    '''
    def __init__(self, fid, json_d=None):
        super(ProcessedFile, self).__init__(fid, json_d=json_d)
        self._parse_processedfile_json()

    def _parse_processedfile_json(self):
        # processed file info
        self.assembly = self.json['assembly']
        self.output_type = self.json['output_type']
        if 'genome_annotation' in self.json:
            self.genome_annotation = self.json['genome_annotation']
            self.attr.update({'genome_annotation': 'Genome Annotation'})
        # update available attributes
        self.attr.update({'assembly': 'Assembly',
                          'output_type': 'Output Type'})
