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

    def simulate(self,f,tq,cst):
        global elapsed_time
        flag = self.service_time>tq
        if flag:
            f.write("t={} p={} slot={} {}".format(elapsed_time,self.pname,tq,"\n"))
            elapsed_time += tq
            self.service_time -= tq
        else:
            f.write("t={} p={} slot={} {}".format(elapsed_time,self.pname,self.service_time,"FINISHED\n"))
            elapsed_time += self.service_time
            self.service_time = 0


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

def simulate1(proc_list,number,tq,cst,out):
    f = open(out,"wb")
    _buffer = [proc_list[i].service_time for i in range(number)]
    while sum(_buffer):
        for i in range(number):
            if proc_list[i].service_time is not 0:
                proc_list[i].simulate(f,tq,cst)
        _buffer = [proc_list[i].service_time for i in range(number)]
    f.close()

def refresh(proc_list,_buffer,number):
    for i in range(number):
        proc_list[i].service_time = _buffer[i]

def main():
    try:
        assert len(sys.argv) == 2
        proc_file = sys.argv[1]

        if not os.path.exists(proc_file):
            raise FileNotFoundError
        f = open(proc_file,"rb")

        number,tq,cst,proc_list = get_params(f)

        proc_list = sorted(proc_list,key=operator.attrgetter("arrival_time"))
        _buffer = [proc_list[i].service_time for i in range(number)]


        simulate1(proc_list,number,tq,cst,"out1")
        refresh(proc_list,_buffer,number)
        #simulate2(proc_list,number,tq,cst,"out2")
        refresh(proc_list,_buffer,number)
        #simulate3(proc_list,number,tq,cst,"out3")
        refresh(proc_list,_buffer,number)
        #simulate4(proc_list,number,tq,cst,"out4")
        '''
        for i in range(number):
            print proc_list[i].service_time
        '''
        f.close()

    except FileNotFoundError:
        print "FileError: File Not Found"
    except AssertionError:
        print "UsageError: Please specify exactly one input file"




if __name__ == "__main__":
    main()
