import os
import sys
import yaml
import glob
import pickle

from config.config_file import ConfigFile
from state.component import MepoComponent

class MepoState(object):

    __state_dir_name = '.mepo'
    __state_fileptr_name = 'state.pkl'

    @staticmethod
    def get_parent_dirs():
        mypath = os.getcwd()
        parentdirs = [mypath]
        while mypath != '/':
            mypath = os.path.dirname(mypath)
            parentdirs.append(mypath)
        return parentdirs

    @classmethod
    def get_dir(cls):
        for mydir in cls.get_parent_dirs():
            state_dir = os.path.join(mydir, cls.__state_dir_name)
            if os.path.exists(state_dir):
                return state_dir
        raise OSError('mepo state dir [.mepo] does not exist')

    @classmethod
    def get_root_dir(cls):
        '''Return directory that contains .mepo'''
        return os.path.dirname(cls.get_dir())

    @classmethod
    def get_file(cls):
        state_file = os.path.join(cls.get_dir(), cls.__state_fileptr_name)
        if os.path.exists(state_file):
            return state_file
        raise OSError('mepo state file [%s] does not exist' % state_file)

    @classmethod
    def exists(cls):
        try:
            cls.get_file()
            return True
        except OSError:
            return False

    @classmethod
    def initialize(cls, project_config_file):
        if cls.exists():
            raise Exception('mepo state already exists')
        input_components = ConfigFile(project_config_file).read_file()
        complist = list()
        for name, comp in input_components.items():
            complist.append(MepoComponent().to_component(name, comp))
        cls.write_state(complist)

    @classmethod
    def read_state(cls):
        if not cls.exists():
            raise Exception('mepo state does not exist')
        with open(cls.get_file(), 'rb') as fin:
            allcomps = pickle.load(fin)
        return allcomps

    @classmethod
    def write_state(cls, state_details):
        if cls.exists():
            state_dir = cls.get_dir()
            pattern = os.path.join(cls.get_dir(), 'state.*.pkl')
            states = [os.path.basename(x) for x in glob.glob(os.path.join(pattern))]
            new_state_id = max([int(x.split('.')[1]) for x in states]) + 1
            state_file_name = 'state.' + str(new_state_id) + '.pkl'
        else:
            state_dir = os.path.join(os.getcwd(), cls.__state_dir_name)
            os.mkdir(state_dir)
            state_file_name = 'state.0.pkl'
        new_state_file = os.path.join(state_dir, state_file_name)
        with open(new_state_file, 'wb') as fout:
            pickle.dump(state_details, fout, -1)
        state_fileptr = os.path.join(state_dir, cls.__state_fileptr_name)
        if os.path.isfile(state_fileptr):
            os.remove(state_fileptr)
        os.symlink(new_state_file, state_fileptr)

