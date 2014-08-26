#!/usr/bin/env python

import sys
import os
import operator

elapsed_time = 0

class FileNotFoundError(Exception):
    pass

class Process(object):
    def __init__(self, pname, service_time, arrival_time):
        self.pname = pname
        self.service_time = service_time
        self.arrival_time = arrival_time

def openfile(f):
    return open(f,"r+")

def get_params(f):
    p = f.readline()
    list = p.split(':')
    number = int(list[1])
    p = f.readline()
    list = p.split(':')
    tq = int(list[1])
    p = f.readline()
    list = p.split(':')
    cst = int(list[1])

    list = []
    proc_list = []

    for i in range(number):
        p = f.readline()
        list = p.split(':')
        pname = list[1]
        service_time = int(list[2])
        arr_time = int(list[3])
        proc = Process(pname, service_time, arr_time)
        proc_list.append(proc)


    return number,tq,cst,proc_list

def simulate1(proc_list,out):
    for i


def main():
    try:
        assert len(sys.argv) == 2
        proc_file = sys.argv[1]

        if not os.path.exists(proc_file):
            raise FileNotFoundError
        f = open(proc_file,"r")

        number,tq,cst,proc_list = get_params(f)

        proc_list = sorted(proc_list,key=operator.attrgetter("arrival_time"))

        '''
        for i in range(number):
            print proc_list[i].arrival_time
        '''
        simulate1(proc_list,number,tq,cst,"out1")
        simulate2(proc_list,number,tq,cst,"out2")
        simulate3(proc_list,number,tq,cst,"out3")
        simulate4(proc_list,number,tq,cst,"out4")

        f.close()

    except FileNotFoundError:
        print "FileError: File Not Found"
    except AssertionError:
        print "UsageError: Please specify exactly one input file"




if __name__ == "__main__":
    main()
