import os

from state.state import MepoState
from utilities import verify

def run(args):
    allcomps = MepoState.read_state()
    if args.comp_name: # single comp name is specified, print relpath
        verify.valid_components([args.comp_name], allcomps)
        for comp in allcomps:
            if comp.name == args.comp_name:
                print(_get_relative_path(comp.local))
    else: # print relpaths of all comps
        max_namelen = len(max([x.name for x in allcomps], key=len))
        FMT = '{:<%s.%ss} | {:<s}' % (max_namelen, max_namelen)
        for comp in allcomps:
            print(FMT.format(comp.name, _get_relative_path(comp.local)))
        
def _get_relative_path(local_path):
    return os.path.relpath(local_path, os.getcwd())
