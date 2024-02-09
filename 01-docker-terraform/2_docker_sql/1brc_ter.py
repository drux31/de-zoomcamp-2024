#!/usr/bin/env python
# coding: utf-8
# author : drux31<contact@lnts.me>
# date 2023-01-25
'''
python version of the 1br challenge
'''
import time
from datetime import timedelta
import csv
import statistics
import multiprocessing as mp
import concurrent.futures as cf
import itertools
import array
import mmap
from collections import defaultdict

txt_file = 'measurements.txt'   

def process_tupple(tupple):
    return (tupple[0], f"{min(tupple[1])}/{round(statistics.mean(tupple[1]), 1)}/{max(tupple[1])}")

def process_file (filename):
     with open(f'data/{filename}', 'r+b') as f:
        for line in f:
            #c,t = line.decode().strip().split(';')
            yield [line.decode().strip().split(';')[0],
                   float(line.decode().strip().split(';')[1])]    

def create_g_cities(filename):
    i= 0
    for val in process_file(filename):
        if val[0] not in cities:
            cities.append(val[0])
            temps.append([val[1]])
        else:
            idx = cities.index(val[0])
            temps[idx].append(val[1])

        i += 1
        if i == 10000000:
            break
    yield list(zip(cities, temps))

def main(txt_file):
    print('\nprocessing measurement file multiprocessing\n')
    
    NB_CPU = 10

    with open(f'data/{txt_file}', 'r+b') as f:
           
        lines = []
        i = 0
        for line in f:
            c,t = line.decode().strip().split(';')
            lines.append([c,float(t)])
            i += 1
            if i == 10000000:
                break
        grouped_cities  = [(k, list(float(x[1]) for x in v)) for (k, v) in itertools.groupby(sorted(lines, key=lambda x: x[0]), lambda x: x[0])]
        agg_mes = list(map(process_tupple, grouped_cities))
        res = {}
        for k, v in agg_mes:
            res[k] = v
        #print (res)
    
        f.close()


if __name__ == "__main__":
    st = time.time()
    main(txt_file)
    en = time.time()
    print('\nend of file processing ; elapsed time: ', timedelta(seconds=en-st), '\n')

    st = time.time()
    cities = []
    temps = []
    i = 0
    
    #print (grouped_cities)
    agg_mes = list(map(process_tupple, sorted(create_g_cities(txt_file))))
    #print(dict(agg_mes))

    en = time.time()
    print('\nend of file processing with yield; elapsed time: ', timedelta(seconds=en-st), '\n')


#https://docs.python.org/3/library/glob.html
#https://docs.python.org/3/library/fileinput.html
#https://docs.python.org/3.12/library/itertools.html#itertools.chain.from_iterable
#https://docs.python.org/3/library/bisect.html
