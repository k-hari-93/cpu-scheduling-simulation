import sys
import os

out1 = "out1"
out2 = "out2"
out3 = "out3"
out4 = "out4"

class FileNotFoundError(Exception):
    pass

class Proc(object):
    def __init__(self, pname, service_time, arrival_time):
        self.pname = pname
        self.service_time = service_time
        self.arrival_time = arrival_time

def main():
    try:
        assert len(sys.argv) == 2
        proc_file = sys.argv[1]
        if not os.path.exists(proc_file):
            raise FileNotFoundError
        f = open(proc_file,"r")

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
            pname = list[0]
            service_time = list[1]
            arr_time = list[2]
            proc = Proc(pname, service_time, arr_time)
            proc_list.append(proc)

        f.close()
    except FileNotFoundError:
        print "FileError: File Not Found"
    except AssertionError:
        print "UsageError: Please specify exactly one input file"




if __name__ == "__main__":
    main()
