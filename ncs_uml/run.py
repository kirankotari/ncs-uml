import sys

from logging import DEBUG
from ncs_uml.main import NcsUml


def check_verbose(params):
    uml = None
    if '-vv' in params:
        uml = NcsUml(level=DEBUG)
        params.remove('-vv')
    if '--verbose' in params:
        uml = NcsUml(level=DEBUG)
        params.remove('--verbose')
    return uml, params


def run():
    uml, params = check_verbose(sys.argv)
    if uml == None: uml = NcsUml()
    
    if len(params) >= 2:
        if 'yang' not in params[1] and params[1] not in uml.options:
            uml.help
        uml.generate(params[1:])
        uml.util.exit
    uml.help

if __name__ == "__main__":
    run()
