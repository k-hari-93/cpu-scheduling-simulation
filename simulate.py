#!/usr/bin/env python

import sys
import os
import operator

elapsed_time = 0

class Process(object):
    def __init__(self, pname, service_time, arrival_time):
        self.pname = pname
        self.service_time = service_time
        self.arrival_time = arrival_time
        self.tr_time = 0
        self.wait_time = 0
        self.wait_flag = 1

    def simulate(self,f,tq,cst,code,check):
        global elapsed_time

        self.wait_flag = 0
        flag = self.service_time>tq

        if flag:
            f.write("{}:{}:{}:{}".format(elapsed_time,self.pname,tq,"NOT FINISHED\n"))
            elapsed_time += tq
            self.service_time -= tq
        else:
            f.write("{}:{}:{}:{}".format(elapsed_time,self.pname,self.service_time,"FINISHED\n"))
            elapsed_time += self.service_time
            self.service_time = 0
            if code == 1 or code == 3:
                self.tr_time = elapsed_time - self.arrival_time
            else:
                self.tr_time = elapsed_time


        if (code == 2 or code == 3) and check:
            f.write("{}:{}:{}:{}".format(elapsed_time,"scheduler",cst,"\n"))
            elapsed_time += cst


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
def test(list,tq):
    count = 0
    l = len(list)
    for i in range(l):
        if list[i] == 0:
            count += 1
    if count == (l-1) and sum(list) <= tq:
        return False
    return True

def simulate(proc_list,number,tq,cst,out,code):
    f = open(out,"ab")
    tr_total = 0.0
    wait_total = 0.0

    _buffer = [proc_list[i].service_time for i in range(number)]

    while sum(_buffer):
        flag = test(_buffer,tq)
        for i in range(number):
            if proc_list[i].service_time is not 0:
                if ((code == 1 or code == 3 ) and elapsed_time >= proc_list[i].arrival_time) or (code == 0 or code == 2):
                    if  proc_list[i].wait_flag:
                        if code == 1 or code == 3:
                            proc_list[i].wait_time = elapsed_time - proc_list[i].arrival_time
                        else:
                            proc_list[i].wait_time = elapsed_time
                    proc_list[i].simulate(f,tq,cst,code,flag)
        _buffer = [proc_list[i].service_time for i in range(number)]
    for i in range(number):
        f.write("TRnd({}) = {}\n".format(proc_list[i].pname,proc_list[i].tr_time))
        tr_total += proc_list[i].tr_time
    f.write("Average TRnd Time : {}\n".format(tr_total/number))
    for i in range(number):
        f.write("W({}) = {}\n".format(proc_list[i].pname,proc_list[i].wait_time))
        wait_total += proc_list[i].wait_time
    f.write("Average Wait Time : {}\n".format(wait_total/number))
    f.close()

def refresh(proc_list,_buffer,number):
    global elapsed_time
    elapsed_time = 0
    for i in range(number):
        proc_list[i].service_time = _buffer[i]
        proc_list[i].tr_time = 0
        proc_list[i].wait_time = 0
        proc_list[i].wait_flag = 1

def main():
    if not len(sys.argv) == 2:
        raise(Exception("Specify exactly one input file"))
    proc_file = sys.argv[1]

    if not os.path.exists(proc_file):
        raise(Exception("No such file"))
    f = open(proc_file,"rb")

    number,tq,cst,proc_list = get_params(f)
    f.close()
    u_buffer = [proc_list[i].service_time for i in range(number)]

    proc_list1 = sorted(proc_list,key=operator.attrgetter("arrival_time"))
    s_buffer = [proc_list1[i].service_time for i in range(number)]

    file_list = ["out1","out2","out3","out4"]
    f = open("out1","w")
    f.write("\tWITHOUT CONSIDERING ARRIVAL TIME OR CONTEXT SWITCH TIME\n");
    f.close()
    f = open("out2","w")
    f.write("\tCONSIDERING ARRIVAL TIME AND WITHOUT CONSIDERING CONTEXT SWITCH TIME\n");
    f.close()
    f = open("out3","w")
    f.write("\tWITHOUT CONSIDERING ARRIVAL TIME AND CONSIDERING CONTEXT SWITCH TIME\n");
    f.close()
    f = open("out4","w")
    f.write("\tCONSIDERING ARRIVAL TIME AND CONTEXT SWITCH TIME\n");
    f.close()

    for i in range(4):
        if i is 0 or i is 2:
            simulate(proc_list,number,tq,cst,file_list[i],i)
            refresh(proc_list,u_buffer,number)
        else:
            simulate(proc_list1,number,tq,cst,file_list[i],i)
            refresh(proc_list1,s_buffer,number)

if __name__ == "__main__":
    main()
