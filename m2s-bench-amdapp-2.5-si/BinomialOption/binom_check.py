#!/usr/bin/python
import re
import glob, os, sys

base_path = "/home/dperoni/approximate_associative_mem/m2s-bench-amdapp-2.5-si/BinomialOption/tested-data/" 
ref_path = "/home/dperoni/approximate_associative_mem/m2s-bench-amdapp-2.5-si/BinomialOption/tested-data/0/16_20.rep"

if len(sys.argv) == 3:
	ref_path = sys.argv[1]
	base_path = sys.argv[2]

reference_file = open(ref_path, 'r'); 

for line in reference_file:
    if "Output" in line:
        data =  reference_file.next()
        break;

#print data

ref_values = re.findall(r"[-+]?\d*\.\d+|\d+", data)
reference_file.close()

#print ref_values
read_file = open(base_path)
check_vals = []

for line in read_file:
    if "Output" in line:
        data = read_file.next()
        
check_vals = re.findall(r"[-+]?\d*\.\d+|\d+", data)

size = min(len(check_vals), len(ref_values))
if(size > 0):
    error = 0;
    for i in range (0, size):
        error += abs((float(ref_values[i]) - float(check_vals[i]))/float(ref_values[i]))*100

    error = error/float(size)
    print error
else:
    print "100"
print "\n"
print "\n"        

