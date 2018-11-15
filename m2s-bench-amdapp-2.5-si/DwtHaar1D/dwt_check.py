#!/usr/bin/python
import re
import glob, os, sys

base_path = "/home/dperoni/Approximate/m2s-bench-amdapp-2.5-si/DwtHaar1D/tested-data/" 
ref_path = "/home/dperoni/Approximate/m2s-bench-amdapp-2.5-si/QuasiRandomSequence/tested-data/0/16.rep"

if len(sys.argv) == 3:
	ref_path = sys.argv[1]
	base_path = sys.argv[2]

reference_file = open(ref_path, 'r'); 

#reference_file = open(ref_path, 'r'); 

#for line in reference_file:
#    if "Output" in line:
#        data =  reference_file.next()
#        break;


#ref_values = re.findall(r"[-+]?\d*\.\d+|\d+", data)
#reference_file.close()

#print ref_values

read_file = open(base_path)
size = 0
error = 0;
for line in read_file:
    if "element" in line:
        data = line
        size += 1
        
        check_vals = re.findall(r"[-+]?\d*\.\d+|\d+", data)

        if(float(check_vals[1]) == 0 and float(check_vals[2]) == 0):
            error += 0
        elif (float(check_vals[1]) == 0):
            error += 100
        else:
            error += abs((float(check_vals[1]) - float(check_vals[2]))/float(check_vals[1]))*100
             


error = error/float(size)
print error
print size
print "\n"
print "\n"

