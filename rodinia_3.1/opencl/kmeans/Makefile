#all: kernel main native main_5
include ../../common/make.config
CC = g++
CC_FLAGS = -g -O2 -m32 -I/opt/AMDAPPSDK-3.0/include/CL/cl.h -I/home/dperoni/approximate_associative_mem_gpu/multi2sim-4.2/runtime/include/CL/cl.h -I/home/dperoni/approximate_associative_mem_gpu/multi2sim-4.2/runtime/include -I/usr/include/x86_64-linux-gnu/c++/4.8/bits/c++config.h -L/home/shepherd/multi2sim/approximate_associative_mem/multi2sim-4.2/lib/.libs -lm2s-opencl -static -pthread -ldl -std=c++11

 



all: main 

native: convnet.h  convolutional_layer.h  fullyconnected_layer.h  layer.h  maxpooling_layer.h  mnist_parser.h  output_layer.h  settings.h  util.h main.cpp cl_wrapper.hpp  timer.hpp filemgt.hpp
	g++ -m32 -o main_native main.cpp -I/opt/AMDAPP/include/ -L/opt/AMDAPP/lib/x86 -lOpenCL -pthread -ldl -std=c++11

main: getopt.h  kmeans.h  unistd.h cluster.o getopt.o read_input.o kmeans_clustering.o rmse.o
	g++ -g -m32 -o kmeans kmeans.cpp cluster.o getopt.o read_input.o kmeans_clustering.o rmse.o -I/home/dperoni/approximate_associative_mem_gpu/multi2sim-4.2/runtime/include -L/home/dperoni/approximate_associative_mem_gpu/multi2sim-4.2/lib/.libs -lm2s-opencl -static -pthread -ldl -std=c++11

main_5: convnet.h  convolutional_layer.h  fullyconnected_layer.h  layer.h  maxpooling_layer.h  mnist_parser.h  output_layer.h  settings.h  util.h main.cpp cl_wrapper.hpp  timer.hpp filemgt.hpp
	g++ -m32 -o main_5 main.cpp -I/home/shepherd/m2s5/multi2sim-5.0/runtime/include -L/home/shepherd/m2s5/multi2sim-5.0/lib/.libs -lm2s-opencl -static -pthread -ldl -std=c++11

kernel: kmeans.cl
	m2c --amd --amd-device Tahiti kmeans.cl # Tahiti: Southern Island

%.o: %.[ch]
	$(CC) $(CC_FLAGS) $< -c

cluster.o: cluster.c 
	$(CC) $(CC_FLAGS) cluster.c -c

getopt.o: getopt.c 
	$(CC) $(CC_FLAGS) getopt.c -c

kmeans.o: kmeans.c 
	$(CC) $(CC_FLAGS) read_input.c -c

rmse.o: rmse.c
	$(CC) $(CC_FLAGS) rmse.c -c

clean:
	rm -f *.o *~ kmeans *.linkinfo kernels.bin
