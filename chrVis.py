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
    output = args.output


    karyotypeFile = cf.get('general','karyotype')
    bandFile = cf.get('general','bandfile')
    scale = cf.getfloat('general','scale')
    viewboxWidth = cf.getint('general','viewboxWidth')
    viewboxHeight = cf.getint('general','viewboxHeight')

    thickness = cf.getfloat('ideogram','thickness')
    bandSize = cf.getfloat('band','thickness')
    label_size = cf.getfloat('ideogram','label_size')
    spacing = cf.getfloat('ideogram','spacing') + thickness


    showBandName = cf.getboolean('band','show_name')


    logger.debug('scale: {}'.format(scale))

    svg = Drawing(debug=True)
    svg.viewbox(width=viewboxWidth,height=viewboxHeight)

    o = svg.rect(insert=(0,0),size=(viewboxWidth,viewboxHeight),stroke_width="5px",stroke="#FFF000",fill="none")


    logger.debug('reading karyotype file')
    dchr = readKaryotype(karyotypeFile)

    logger.debug('{} chromosomes to draw'.format(len(dchr)))

    suggestSpacing = int((viewboxWidth) / (len(dchr)+1)) - thickness

    logger.debug('Calculate prefer spacing is {}. You use {}'.format(suggestSpacing,spacing-thickness))

    logger.debug('reading band file')
    dband = readBand(bandFile)
    


    
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

        svgObj.set_labelSize(11)
        svgObj.set_bandSize(bandSize)
        svgObj.set_showBandName(showBandName)
        svgObj.set_spacing(spacing)
        svgObj.set_thickness(thickness)


        e = svgObj.getCode()

        this = svg.add(e)
    this = svg.add(o)

    outputCode = svg.tostring()

    with open(output,'w') as ofh:
        ofh.write(outputCode)
        logger.info('Done!')




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-c','-conf', '--conf', type=str,default = None, help='configure file')
    parser.add_argument('-o','-out','--output',type =str , default = None, help='output filename')
    args = parser.parse_args()
    if args.conf is None:
        parser.print_help()
        sys.exit()

    main(args)

