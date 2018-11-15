#all: kernel main native main_5
include ../../common/make.config
CC = g++
CC_FLAGS = -g -O2 -m32 -lm2s-opencl -static -pthread -ldl -std=c++11

INCLUDES = -I/opt/AMDAPPSDK-3.0/include/CL/cl.h -I/home/dperoni/approximate_associative_mem_gpu/multi2sim-4.2/runtime/include/CL/ -I/home/dperoni/approximate_associative_mem_gpu/multi2sim-4.2/runtime/include -I/usr/include/x86_64-linux-gnu/c++/4.8/bits/ -L/home/dperoni/approximate_associative_mem_gpu/multi2sim-4.2/lib/.libs

all: main 


main: backprop.o imagenet.o facetrain.o
	$(CC) $(CC_FLAGS) -o backprop backprop_ocl.cpp backprop.o imagenet.o facetrain.o $(INCLUDES) -lm2s-opencl -static -pthread -ldl -std=c++11


kernel: Kernels.cl
	m2c --amd --amd-device Tahiti Kernels.cl # Tahiti: Southern Island

%.o: %.[ch]
	$(CC) $(CC_FLAGS) $< -c

backprop.o: backprop.c 
	$(CC) $(CC_FLAGS) $(INCLUDES) backprop.c -c
	
facetrain.o: facetrain.c
	$(CC) $(CC_FLAGS) $(INCLUDES) facetrain.c -c

imagenet.o: imagenet.c
	$(CC) $(CC_FLAGS) $(INCLUDES) imagenet.c -c


clean:
	rm -f *.o *~ guassian *.linkinfo gaussian.bin

