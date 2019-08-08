#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import configparser
from svgwrite import *
from operator import itemgetter
from collections import OrderedDict
from itertools import groupby


class VectorChr:
    """docstring for ClassName"""

    chrcount = 0

    def __init__(self,chrName,chrValue,bands,scale,labelSize = 22,
                annoSize = 10, 
                margin = 50,
                thickness = 20,
                showBandName = False
                ):

        self.chrName = chrName
        self.chrValue = chrValue
        self.bands = bands
        self.thickness = thickness
        self.spacing = 100
        self.bandSize = 20
        self.showBandName = showBandName
        self.margin = margin
        self.labelSize = labelSize
        self.annoSize = annoSize
        self.scale = scale
        self.svg = Drawing()

        VectorChr.chrcount += 1

    def set_bandSize(self, Size):
        self.bandSize=Size

    def set_labelSize(self, labelSize):
        self.labelSize=labelSize

    def set_spacing(self, spacing):
        self.spacing=spacing

    def set_thickness(self, thickness):
        self.thickness=thickness

    def set_showBandName(self, showBandName):
        self.showBandName=showBandName

    def get_chrCount(self):
        return self.chrcount

    def get_chrName(self):
        return self.chrName

    def get_groupElement(self):

        svg = self.svg
        svgGroup = svg.g(id=self.get_chrName(), stroke='green')
        return svgGroup



    def getCode(self):

        svg = self.svg
        svgGroup = self.get_groupElement()

        thisGroup = svg.add(svgGroup)



        x = self.spacing*self.chrcount
        y = int(self.chrValue['length']) / int(self.scale)

        # print "y:" + str(y)


        chrBackbone = self.get_chrBackbone(x,y,self.margin,color = self.chrValue["color"])
        chrTitle = self.get_chrTitle(x,30,self.labelSize)

        thisGroup.add(chrBackbone)
        thisGroup.add(chrTitle)

        if self.bands:
            for n, i in enumerate(self.bands):
                y1 = int(i[2]) / self.scale
                y2 = int(i[3]) / self.scale

                startY = min(y1,y2)
                endY = abs(y1-y2)


                # Draw gene band

                p = svg.rect(insert=(x-10+1, startY + self.margin ), size=(self.bandSize-2, endY),
                        fill=i[4], stroke='black', stroke_width=0,opacity=1)

                # Draw gene annotation

                offset = 5

                if self.showBandName:

                    mark = svg.polyline(points=[(x+15,startY+self.margin + offset),(x+20,startY+self.margin + offset),
                                                (x+25,startY+self.margin + offset - 10),(x+30,startY+self.margin + offset - 10),]
                                        ,stroke='blue',fill="none")

                    ann = svg.text(i[1],insert=(x+35,startY+self.margin + offset - 10),stroke_width=0,fill="black",font_size=13)
                    thisGroup.add(mark)
                    thisGroup.add(ann)
                thisGroup.add(p)

        thisGroup.add(chrBackbone)


        return thisGroup



    def get_chrBackbone(self,x,y,margin = 30, color='black'):
        '''
        返回染色体的染色体框架
        '''

        #线型
        v = self.svg.line(start=(x,margin),end=(x,y+margin),stroke=color,stroke_width="3px")

        #rect
        v = self.svg.rect(insert=(x-10,margin), size=(self.thickness, y), fill="none",stroke=color,stroke_width="1px")

        return v



    def get_chrTitle(self, x, y = 25,labelSize=16, color='blue'):
        '''
        染色体名称
        '''

        v = self.svg.text(self.chrName,insert=(x - 15 ,y),stroke_width=0,fill="black",font_size=labelSize)
        return v



def readKaryotype(fname):
    '''
    karyotype file
    ------------------------------
    chrName    length    #FFFFFF
     '''

    d = OrderedDict()
    with open(fname) as f:
        rows = [x.strip().split() for x in f]

    for row in rows:
        d[row[0]] = {'name':row[1], 'length': row[2], 'color': row[3]}

    return d


def readBand(handle):
    '''
    读取染色体上基因信息文件，格式为：
    chrName    geneName    pos    #FFF(颜色代码)
    '''

    d = {}
    with open(handle) as f:
        rows = [x.strip().split() for x in f]
        rows.sort(key=itemgetter(0))
        groups = groupby(rows, lambda x: x[0])
        for k,v in groups:
            d[k] = list(v)
 
    return d
