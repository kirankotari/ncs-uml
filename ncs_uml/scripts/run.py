#!/usr/bin/env python
from __future__ import absolute_import
from logging import INFO, DEBUG
import optparse

import ncs_uml
from ncs_uml.main import NcsUml


def get_options():
    usage = f"""{ncs_uml.__name__} [options] [<filename>...]

Creates plantUML file for the YANG module in <filename>, and all its dependencies.
It can be converted into PNG/SVG images using www.plantuml.com or with editor plugins."""

    optlist = [
        # use capitalized versions of std options help and version
        optparse.make_option("-h", "--help",
                             action="help",
                             help="Show this help message and exit"),
        optparse.make_option("-v", "--version",
                             action="version",
                             help="Show version number and exit"),
        optparse.make_option("-V", "--verbose",
                             action="store_true"),
        optparse.make_option("--skip",
                             dest="skip",
                             default=[],
                             action="append",
                             help="skip given yang modules"),
        optparse.make_option("--skip-grouping",
                             dest="skip_grouping",
                             action="store_true"),
        optparse.make_option("--dpath",
                             dest="dpath",
                             default=[],
                             action="append",
                             help="dependent yang module paths"),
    ]
    optparser = optparse.OptionParser(usage, add_help_option = False)
    optparser.version = f'{ncs_uml.__name__} {ncs_uml.__version__}'
    optparser.add_options(optlist)

    return optparser


def run():
    optparser = get_options()
    (o, args) = optparser.parse_args()
    uml = None
    if o.verbose:
        uml = NcsUml(o, level=DEBUG)
    else:
        uml = NcsUml(o, level=INFO)

    if len(args) > 1:
        uml.log.error("too many files to convert\n")
        uml.util.exit

    if len(args) == 0:
        uml.log.error("missing yang file in the command\n")
        optparser.print_help()
        uml.util.exit

    if 'yang' not in args[0]:
        uml.log.error("invalid yang file given\n")
        uml.util.exit

    uml.generate(args[0])
