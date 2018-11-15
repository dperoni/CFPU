#!/usr/bin/python
import re
import glob, os, sys

base_path = "/home/dperoni/approximate_associative_mem/m2s-bench-amdapp-2.5-si/BinomialOption/tested-data/" 
base_path = "/home/dperoni/rodinia_3.1/opencl/nn/tested-data/0.0625/" 
ref_path = "/home/dperoni/rodinia_3.1/opencl/nn/tested-data/0/0-0/_1000.rep"

if len(sys.argv) == 3:
	ref_path = sys.argv[1]
	base_path = sys.argv[2]

reference_file = open(ref_path, 'r'); 

i = 0;
ref_values = []

for line in reference_file:
	#print line    
	if "Distance" in line:
		#print "here\n"
	
        	ref_values.append(re.findall(r"[-+]?\d*\.\d+|\d+", line)[0])
		i += 1

#print data

reference_file.close()

#print ref_values

read_file = open(base_path)
check_vals = []
for line in read_file:
    if "Distance=" in line:
        data = line
        check_vals.append(re.findall(r"[-+]?\d*\.\d+|\d+", data)[0])




       
size = len(check_vals)
#print check_vals
if(size > 0):
	error = 0;
	#print ref_values
	for i in range (0, size):
	    error += abs((float(ref_values[i]) - float(check_vals[i]))/float(ref_values[i]))*100

	error = error/float(size)
	print error
else:
	print "100"
	print "\n"
	print "\n"        

