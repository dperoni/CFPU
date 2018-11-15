#all: kernel main native main_5
include ../../common/make.config
CC = g++
CC_FLAGS = -g -O2 -m32 -lm2s-opencl -static -pthread -ldl -std=c++11

INCLUDES = -I/home/dperoni/approximate_associative_mem_gpu/multi2sim-4.2/runtime/include/CL/cl.h -I/home/dperoni/approximate_associative_mem_gpu/multi2sim-4.2/runtime/include -I/usr/include/x86_64-linux-gnu/c++/4.8/bits/c++config.h -L/home/dperoni/approximate_associative_mem_gpu/multi2sim-4.2/lib/.libs

all: main 


main: 
	$(CC) $(CC_FLAGS) -o nn $(INCLUDES) nearestNeighbor.cpp utils.cpp clutils.cpp -lm2s-opencl -static -pthread -ldl -std=c++11


kernel: lud_kernel.cl
	m2c --amd --amd-device Tahiti lud_kernel.cl # Tahiti: Southern Island

%.o: %.[ch]
	$(CC) $(CC_FLAGS) $< -c

clean:
	rm -f *.o *~ dwt2d *.linkinfo dwt2d.bin

