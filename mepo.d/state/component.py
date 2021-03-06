import os
from collections import namedtuple
from utilities.version import MepoVersion

class MepoComponent(object):

    __slots__ = ['name', 'local', 'remote', 'version', 'develop', 'sparse', 'recurse_submodules']

    def __init__(self):
        self.name = None
        self.local = None
        self.remote = None
        self.version = None
        self.develop = None
        self.sparse = None
        self.recurse_submodules = None

    def __repr__(self):
        return '{} - local: {}, remote: {}, version: {}, develop:{}'.format(
            self.name, self.local, self.remote, self.version, self.develop)

    def __set_original_version(self, comp_details):
        if comp_details.get('branch', None):
            # SPECIAL HANDLING of 'detached head' branches
            ver_name = 'origin/' + comp_details['branch']
            ver_type = 'b'
        else:
            ver_name = comp_details['tag'] # 'tag' key has to exist
            ver_type = 't'
        self.version = MepoVersion(ver_name, ver_type, True)
        
    def to_component(self, comp_name, comp_details):
        self.name = comp_name
        self.local = os.path.abspath(comp_details['local'])
        self.remote = comp_details['remote']
        self.develop = comp_details.get('develop', None) # develop is optional
        self.sparse = comp_details.get('sparse', None) # sparse is optional
        self.recurse_submodules = comp_details.get('recurse_submodules', None) # recurse_submodules is optional
        self.__set_original_version(comp_details)
        return self

    def to_dict(self, start):
        details = dict()
        details['local'] = './' + os.path.relpath(self.local, start)
        details['remote'] = self.remote
        if self.version.type == 't':
            details['tag'] = self.version.name
        else: # if not tag, version has to be a branch
            if self.version.detached: # SPECIAL HANDLING of 'detached head' branches
                details['branch'] = self.version.name.replace('origin/', '')
            else:
                details['branch'] = self.version.name
        if self.develop:
            details['develop'] = self.develop
        if self.sparse:
            details['sparse'] = self.sparse
        if self.recurse_submodules:
            details['recurse_submodules'] = self.recurse_submodules
        return {self.name: details}
