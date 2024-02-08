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

def process_row_lock(chunk, conn, l):
    l.acquire()
    try:
        cities = {}
        #final_data_set = {}
        #i = 0
        for row in chunk:
            #print (row)
            city, temp = row
            if city.strip() not in cities:
                cities[city.strip] = [float(temp)]
            else:
                cities[city].append(float(temp))
            
            #i += 1
            #if i == 10000000:
            #    break

        #for city in cities:
            #c_mean = round(statistics.mean(cities[city]), 1)
        #    final_data_set[city] = f"{min(cities[city])}/{round(statistics.mean(cities[city]), 1)}/{max(cities[city])}"

        conn.send(cities)
    finally:
        l.release()

def process_row_no_lock(csv_obj, conn):
    cities = {}
    i = 0
    for row in csv_obj:
        if row[0].strip() not in cities:
            cities[row[0].strip()] = [float(row[1])]
        else:
            cities[row[0].strip()].append(float(row[1]))    
        i += 1
        if i == 100000000:
            break
    conn.send(dict(sorted(cities.items())))

def process_row(chunk):
    cities = {}
    #final_data_set = {}
    #i = 0
    for row in chunk:
        #print (row)
        city, temp = row
        if city.strip() not in cities:
            cities[city.strip] = [float(temp)]
        else:
            cities[city].append(float(temp))
        
        #i += 1
        #if i == 10000000:
        #    break

    #for city in cities:
        #c_mean = round(statistics.mean(cities[city]), 1)
    #    final_data_set[city] = f"{min(cities[city])}/{round(statistics.mean(cities[city]), 1)}/{max(cities[city])}"
    print(len(cities))

def process_tupple(tupple):
    return (tupple[0], f"{min(tupple[1])}/{round(statistics.mean(tupple[1]), 1)}/{max(tupple[1])}")


def main():
    txt_file = 'measurements.txt'   
    print('\nprocessing measurement file multiprocessing\n')
    
    NB_CPU = 10

    with open(f'data/{txt_file}', 'r+b') as f:
        
        
        '''
        #mm = mmap.mmap(f.fileno(), 0)
        barr = []
        i = 0
        while i < 100000000:
            barr.append(f.readline())
            i += 1
        
        print(barr[0])
        #print(f.readline())
        '''
        
        
        lines = []
        i = 0
        for line in f:
            c,t = line.decode().strip().split(';')
            lines.append([c,float(t)])
            i += 1
            if i == 1000:
                break
        grouped_cities  = [(k, list(float(x[1]) for x in v)) for (k, v) in itertools.groupby(sorted(lines, key=lambda x: x[0]), lambda x: x[0])]
        agg_mes = list(map(process_tupple, grouped_cities))
        res = {}
        for k, v in agg_mes:
            res[k] = v
        print (res)
                               
        #f.seek(2000001)
        
        #print(f.read())

        f.close()
        #csv_obj = csv.reader(f, delimiter=';') 
        #file_chunks = list(itertools.batched(csv_obj, 1000))     
        #print(file_chunks[0])
        #parent_con, child_con = mp.Pipe()
        #pool = cf.ProcessPoolExecutor(max_workers=6)
        #result = list(pool.map(process_row, file_chunks))
        #print(result[0])
        #map(process_row, file_chunks)
        #f.close()
        #lines = f.readlines()

        #arr1 = lines[:int(len(lines)/4)]
        #arr2 = lines[int(len(lines)/4):int(len(lines)/2)]
        #arr3 = lines[int(len(lines)/2):-int(len(lines)/4)]
        #arr4 = lines[-int(len(lines)/4):]

        #test = {}
        #print(len(arr1), len(arr2), len(arr3), len(arr4), )
        #tf = None
        #for a in arr1:
        #    c,t = a.decode().strip().split(';')
        #    tf = c
        #    if c in test.keys():
        #        test[c].append(float(t))
        #    else:
        #        test[c]=[float(t)]
        
        #res = {}
        #for c in test :
        #    res[c] = f"{min(test[c])}/{round(statistics.mean(test[c]), 1)}/{max(test[c])}"

        #print(len(test))
        #print (len(res))
        
        #for k in res:
        #    print (k, res[k])
        #print(res)
            
        '''
        lock = mp.Lock()
        for chunk in file_chunks:
            p = mp.Process(target=process_row_lock, args=(chunk, child_con, lock))
            p.start()
            temp_dict = parent_con.recv()
            p.join()
        f.close()
        
        j = 0
        print(len(temp_dict))
        for f in temp_dict:
            print(f, f"{min(temp_dict[f])}/{round(statistics.mean(temp_dict[f]), 1)}/{max(temp_dict[f])}")
            j += 1
            if j == 10:
                break
        '''

if __name__ == "__main__":
    st = time.time()
    main()
    en = time.time()
    print('\nend of file processing ; elapsed time: ', timedelta(seconds=en-st), '\n')

#https://docs.python.org/3/library/glob.html
#https://docs.python.org/3/library/fileinput.html
#https://docs.python.org/3.12/library/itertools.html#itertools.chain.from_iterable
#https://docs.python.org/3/library/bisect.html
