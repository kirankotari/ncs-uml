import sys
import ncs_uml
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
    if len(params) < 2:
        print(uml.help)
        uml.util.exit

    if len(params) >= 2:
        p, v = False, False
        for i in params:
            if 'yang' in i:
                p = True
            if '-v' == i or '--version' == i:
                v = True

        if p:
            uml.generate(params[1:])
            uml.util.exit
        elif v:
            print(f'ncs-uml version {ncs_uml.__version__}')
            uml.util.exit
        else:
            print(uml.help)

if __name__ == "__main__":
    run()
