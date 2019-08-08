# -*- coding: utf-8 -*-

# from pysvg.structure import *
# from pysvg.chromose import *
from svgwrite import *
from framework import *
import sys
import argparse
import logging
import configparser
import pprint

pp = pprint.PrettyPrinter(indent=4)

logging.basicConfig(level = logging.DEBUG,format = '[%(levelname)s] - %(name)s -> %(message)s')
logger = logging.getLogger(__name__)


def main(args):
    cf = configparser.ConfigParser()
    cf.read(args.conf)

    karyotypeFile = cf.get('general','karyotype')
    bandFile = cf.get('general','bandfile')
    scale = cf.getfloat('general','scale')
    imgWidth = cf.getint('general','imgWidth')
    imgHeight = cf.getint('general','imgHeight')

    thickness = cf.getfloat('ideogram','thickness')
    bandSize = cf.getfloat('band','thickness')
    label_size = cf.getfloat('ideogram','label_size')
    spacing = cf.getfloat('ideogram','spacing') + thickness


    showBandName = cf.getboolean('band','show_name')


    logger.debug('scale: {}'.format(scale))

    svg = Drawing(debug=True)
    svg.viewbox(width=1400,height=900)


    logger.debug('reading karyotype file')
    dchr = readKaryotype(karyotypeFile)

    logger.debug('{} chromosomes to draw'.format(len(dchr)))

    logger.debug('reading band file')
    dband = readBand(bandFile)
    # pp.pprint(dband)
    
    for chrName,chrValue in dchr.items():
        logger.info('processing {}'.format(chrName))

        if chrName in dband:
            bandNow = dband[chrName]
        else:
            bandNow = []
            logger.warning('{} have no band info.'.format(chrName))

        svgObj = VectorChr(
            chrValue['name'],chrValue,bandNow,scale
            )

        svgObj.set_labelSize(16)
        svgObj.set_bandSize(bandSize)
        svgObj.set_showBandName(showBandName)
        svgObj.set_spacing(spacing)
        svgObj.set_thickness(thickness)


        e = svgObj.get_svg()

        this = svg.add(e)


    p = svg.tostring()
    print(p)




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-c', '--conf', type=str,default = None, help='configure file')
    parser.add_argument('-o','--out',type =str , default = None, help='output filename')
    args = parser.parse_args()
    if args.conf is None:
        parser.print_help()
        sys.exit()

    main(args)

