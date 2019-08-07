#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from svgwrite import *
from operator import itemgetter
from itertools import groupby

class vectorChr:
    '''
    class
    '''
    chrcount = 0

    def __init__(self,chrName,chrValue,bands,scalefactor,titleSize = 22, annoSize = 10, margin = 50):
        self.chrName = chrName
        self.chrValue = chrValue
        self.bands = bands
        self.margin = margin
        self.titleSize = titleSize
        self.annoSize = annoSize
        self.scalefactor = scalefactor
        self.svg = Drawing()
        vectorChr.chrcount += 1

    def set_titleSize(self, titleSize):
        self.titleSize=titleSize


    def get_titleSize(self, titleSize):
        return self.titleSize


    def get_chrCount(self):
        return self.chrcount


    def get_chrName(self):
        return self.chrName



    def get_groupElement(self):

        svg = self.svg

        svgGroup = svg.g(id=self.get_chrName(), stroke='green')

        return svgGroup





    def get_svg(self):

        svg = self.svg
        svgGroup = self.get_groupElement()

        thisGroup = svg.add(svgGroup)



        x = 100*self.chrcount
        y = int(self.chrValue['length']) / int(self.scalefactor)

        # print "y:" + str(y)


        chrBackbone = self.get_chrBackbone(x,y,self.margin,color = self.chrValue["color"])
        chrTitle = self.get_chrTitle(x,30,self.titleSize)

        thisGroup.add(chrBackbone)
        thisGroup.add(chrTitle)

        if self.bands:
            for n, i in enumerate(self.bands):
                y1 = int(i[2]) / self.scalefactor
                y2 = int(i[3]) / self.scalefactor



                # Draw gene band

                p = svg.rect(insert=(x-10+1, y1 + self.margin ), size=(20-2, y2),
                        fill=i[4], stroke='black', stroke_width=0,opacity=0.5)

                # Draw gene annotation

                offset = 5

                mark = svg.polyline(points=[(x+15,y1+self.margin + offset),(x+20,y1+self.margin + offset),
                                            (x+25,y1+self.margin + offset - 10),(x+30,y1+self.margin + offset - 10),]
                                    ,stroke='blue',fill="none")

                ann = svg.text(i[1],insert=(x+35,y1+self.margin + offset - 10),stroke_width=0,fill="black",font_size=13)

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
        v = self.svg.rect(insert=(x-10,margin), size=(20, y + margin), fill="none",stroke=color,
                          stroke_width="2px",rx="8px",ry="10px")

        return v



    def get_chrTitle(self, x, y = 25,titleSize=16, color='blue'):
        '''
        染色体名称
        '''

        v = self.svg.text(self.chrName,insert=(x - 15 ,y),stroke_width=0,fill="black",font_size=titleSize)
        return v



    def get_chrBands(self):
        '''
        标注染色体上的基因
        '''

        pass






def read_chr(handle):
    '''
    读取染色体长度文件，格式为：
    chrName    length    #FFF(颜色代码)
     '''
    d = OrderedDict()

    with open(handle) as f:
        rows = [x.strip().split() for x in f]

    for row in rows:
        d[row[0]] = {'length': row[1], 'color': row[2]}

    return d



def read_cds(handle):
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





def getScaleFactor(chrdict):
    '''
    计算染色体缩放的参数
    '''
    count = 0
    totalLength = 0

    for k, v in chrdict.items():
        count += 1
        totalLength += int(v['length'])

    scale = totalLength / count / int(400)

    return scale



























