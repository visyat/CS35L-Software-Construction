#!/usr/bin/python

"""
Shuffles the input and produces a random permutation of the the lines of an in
put file

Vishal Yathish
COM SCI 35L

"""

import random, sys
import argparse 

class shuf:
    def __init__ (self, filename=''):
        if (filename != ''):
            f = open(filename, 'r')
            self.lines = f.readlines()
            f.close()

    def function_body (self, list, head, repeat, addNewlines=False): 
        if (repeat):
            if head > 0: 
                for i in range (head):
                    sys.stdout.write(random.choice(list))
                    if (addNewlines): sys.stdout.write('\n') 
            else:
                while True: 
                    sys.stdout.write(random.choice(list))
                    if (addNewlines): sys.stdout.write('\n') 
        else: 
            random.shuffle(list)
            if head > 0: 
                for i in range (head):
                    sys.stdout.write(list[i])
                    if (addNewlines): sys.stdout.write('\n') 
            else: 
                for i in list:
                    sys.stdout.write(i)
                    if (addNewlines): sys.stdout.write('\n') 

    def default (self, head=0, repeat=False): 
        self.function_body (self.lines, head, repeat)
    
    def echo(self, args, head=0, repeat=False):
        self.function_body(args, head, repeat, True)

    def input_range (self, lower_bound, upper_bound, head=0, repeat=False):
        int_range = [str(i) for i in range (lower_bound, upper_bound+1)]
        self.function_body(int_range, head, repeat, True)

    def no_args (self): 
        lines = [line for line in sys.stdin]
        self.function_body(lines, 0, False)
    
def main(): 
    usage_msg = """%prog [OPTION]... FILE

Outputs a random permutation of the input file's lines."""

    parser = argparse.ArgumentParser(usage=usage_msg)
    parser.add_argument("-e", "--echo", 
                        dest="echo", action="store_true",
                        help="Treat each command-line operand as an input line.")
    parser.add_argument("-i", "--input-range", 
                        dest="inputrange", action="store", nargs=1,
                        help="Act as if input came from a file containing the range of unsigned decimal integers lo...hi, one per line.")
    parser.add_argument("-n", "--head-count", 
                        dest="headcount", nargs=1,
                        help="Output at most count lines. By default, all input lines are output.")
    parser.add_argument("-r", "--repeat-count", 
                        dest="repeat", 
                        action="store_true",
                        help="Repeat output values, that is, select with replacement.")
    options, args = parser.parse_known_args()

    if (options.echo and bool(options.inputrange)):
        parser.error("shuf: cannot combine -e and -i options")
    if options.headcount:
        if int(options.headcount[0]) < 0: 
            parser.error("shuf: invalid value for headcount")
    try: 
        if options.headcount:
            h=int(options.headcount[0])
        else:
            h=0
    except ValueError:
        parser.error("shuf: invalid value for headcount")

    r=False
    if options.repeat: r=True

    if (options.echo):
        generator = shuf()
        generator.echo(args,h,r)
    elif (options.inputrange): 
        generator = shuf()
        lower_bound, upper_bound = int(options.inputrange[0][0]), int(options.inputrange[0][2:])
        generator.input_range(lower_bound, upper_bound, h, r)
    elif (args==[] or args[0]=='-'):
        generator = shuf()
        generator.no_args()
    else:
        generator = shuf(args[-1])
        generator.default(h,r)

if __name__ == "__main__":
    main()
