# chrVis
Visualize genes on chromesome

## Usage

```
usage: main.py [-h] [-o OUTPUT] [-wi WIDTH] [-hi HEIGHT] [-f FONTSIZE]
               chr gene

positional arguments:
  chr                   chr file
  gene                  gene file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output filename
  -wi WIDTH, --width WIDTH
                        width of the image
  -hi HEIGHT, --height HEIGHT
                        height of the image
  -f FONTSIZE, --fontsize FONTSIZE
                        font size

```

## sample chr file

Three columns `chromesome name` , `chromosome length`, `chromosome color`


```
chr1    2000000 #333300
chr2    1400012 #333300
chr3    1900000 #333300
```


## sample gene file

Four columns `chromesome name` , `gene name`,`gene position`, `color`

```
chr1	gene1	1000	#666666
chr2	gene2	100030	#99CC00
chr1	gene3	400000	#0066CC
chr1	gene4	50400	#99CC66
chr1	gene5	600000	#003366
```

## sample output

![sample output](./sample_output.svg)
