import sys

tq = 15
cst = 5

class Process(object):
    def __int__(self, pname,service_time, arrival_time):
        self.pname = pname
        self.service_time = service_time
        self.arrival_time = arrival_time

def main():
    try:
        assert len(sys.argv) == 2
        proc_file = sys.argv[1]
        print proc_file

    except AssertionError:
        print "\nUsageError:Please specify exactly one input file.\n"


if __name__ == "__main__":
    main()
