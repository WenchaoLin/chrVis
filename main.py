# -*- coding: utf-8 -*-

# from pysvg.structure import *
# from pysvg.chromose import *
from chrVis import *
from svgwrite import *
import sys
import argparse




def draw(filename):
    '''主程序入库
    '''

    svg = Drawing(filename=filename, size=(args.width,args.height),debug=True)


    chrs = read_chr(args.chr)
    genes = read_cds(args.gene)
    scalefactor = getScaleFactor(chrs)

    for chrName,chrValue in chrs.items():
        if genes.get(chrName):
            gene = genes[chrName]
        else:
            gene = []

        
        svgGroup = vectorChr(chrName,chrValue,gene,scalefactor)
        svgGroup.set_titleSize(22)

        e = svgGroup.get_svg()

        this = svg.add(e)
    if filename:
        svg.save()
    else:      
        p = svg.tostring()
        print p
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('chr', help='chr file')
    parser.add_argument('gene', help='gene file')
    parser.add_argument('-o','--output',type =str , default = None,help='output filename')
    parser.add_argument('-wi', '--width', type=str,
                        default='400px', help='width of the image')
    parser.add_argument('-hi', '--height', type=str,
                        default='600px', help='height of the image')
    parser.add_argument('-f', '--fontsize', default='8', help='font size')
    args = parser.parse_args()
    if args.chr is None:
        parser.print_help()
        sys.exit()

    draw(args.output)

