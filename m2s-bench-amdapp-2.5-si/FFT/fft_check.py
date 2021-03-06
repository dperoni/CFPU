#!/usr/bin/python
import re
import glob, os, sys


base_path = "/home/dperoni/Approximate/m2s-bench-amdapp-2.5-si/FFT/tested-data/" 
ref_path = "/home/dperoni/Approximate/m2s-bench-amdapp-2.5-si/FFT/tested-data/0/16.rep"

if len(sys.argv) == 3:
	ref_path = sys.argv[1]
	base_path = sys.argv[2]


reference_file = open(ref_path, 'r'); 

for line in reference_file:
    if "verification Output img" in line:
        data =  reference_file.next()
        break;


ref_values = re.findall(r"[-+]?\d*\.\d+|\d+", data)
reference_file.close()

#print ref_values

read_file = open(base_path)
check_vals = []
for line in read_file:
    if "Output img" in line and not "verification" in line:
        data = read_file.next()
    if "verification Output img" in line:
        refs =  read_file.next()

check_vals = re.findall(r"[-+]?\d*\.\d+|\d+", data)
ref_values = re.findall(r"[-+]?\d*\.\d+|\d+", refs)

size = len(check_vals)
if(size > 0):
    error = 0;
    for i in range (0, size):
        if(float(ref_values[i]) == 0 and float(check_vals[i]) == 0):
            error += 0
        elif (float(ref_values[i]) == 0):
            error += 100
        else:
            error += abs((float(ref_values[i]) - float(check_vals[i]))/float(ref_values[i]))*100

    error = error/float(size)
    print error
else:
    print "100"
print "\n"
print "\n"        

