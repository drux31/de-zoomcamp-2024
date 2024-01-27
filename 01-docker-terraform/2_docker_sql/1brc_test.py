#!/usr/bin/env python
# coding: utf-8
# author : drux31<contact@lnts.me>
# date 2023-01-25
'''
python version of the 1br challenge
'''
from timeit import default_timer as timer
from datetime import timedelta
import csv
import statistics
import multiprocessing as mp

def process_row(csv_obj, conn, l):
    l.acquire()
    try:
        cities = {}
        final_data_set = {}
        i = 0
        for row in csv_obj:
            if row[0].strip() not in cities:
                cities[row[0].strip()] = [float(row[1])]
            else:
                cities[row[0].strip()].append(float(row[1]))
            
            i += 1
            if i == 10000000:
                break

        for city in cities:
            #c_mean = round(statistics.mean(cities[city]), 1)
            final_data_set[city] = f"{min(cities[city])}/{round(statistics.mean(cities[city]), 1)}/{max(cities[city])}"

        conn.send(dict(sorted(final_data_set.items())))
    finally:
        l.release()

def process_row_no_lock(csv_obj, conn):
    cities = {}
    i = 0
    for row in sorted(csv_obj):
        if row[0].strip() not in cities:
            cities[row[0].strip()] = [float(row[1])]
        else:
            cities[row[0].strip()].append(float(row[1]))    
        i += 1
        if i == 100000000:
            break
    conn.send(dict(sorted(cities.items())))

'''
def process_row_bis(row, conn):
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
'''

def main():
    txt_file = 'measurements.txt'   
    print('\nprocessing measurement file multiprocessing')
    with open(f'data/{txt_file}', 'r') as f:
        csv_obj = csv.reader(f, delimiter=';')       

        start = timer()

        parent_con, child_con = mp.Pipe()
        lock = mp.Lock()

        p = mp.Process(target=process_row_no_lock, args=(csv_obj, child_con))
        p.start()
        temp_dict = parent_con.recv()
        p.join()
        f.close()
        end = timer()

        print('end of file processing ; elapsed time: ', timedelta(seconds=end-start), '\n')
        j = 0
        for f in temp_dict:
            print(f, f"{min(temp_dict[f])}/{round(statistics.mean(temp_dict[f]), 1)}/{max(temp_dict[f])}")
            j += 1
            if j == 10:
                break
        # https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query


if __name__ == "__main__":
    main()

