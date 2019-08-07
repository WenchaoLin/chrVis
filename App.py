# -*- coding: utf-8 -*-

# from pysvg.structure import *
# from pysvg.chromose import *
from svgwrite import *
from framework import *
import sys
import argparse
import logging
import ConfigParser
import pprint

pp = pprint.PrettyPrinter(indent=4)

logging.basicConfig(level = logging.DEBUG,format = '[%(levelname)s] line:%(lineno)d in %(name)s -> %(message)s')
logger = logging.getLogger(__name__)

def main(args):
    cf = ConfigParser.ConfigParser()
    cf.read(args.conf)
    karyotypeFile = cf.get('main','karyotype')
    bandFile = cf.get('main','bandfile')
    logger.debug('reading karyotype file')
    dchr = readKaryotype(karyotypeFile)
    logger.debug('reading band file')
    dband = readBand(bandFile)
    



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-c', '--conf', type=str,default = None, help='configure file')
    parser.add_argument('-o','--out',type =str , default = None, help='output filename')
    args = parser.parse_args()
    if args.conf is None:
        parser.print_help()
        sys.exit()

    main(args)

