# C compiler
#CC = clang
CC = clang_wrapper.py
CC_FLAGS = -g -fopenmp  -O3  --use-clang -std=c99 -Wno-error=implicit-function-declaration -Wno-error=implicit-int  -ffinite-math-only -fno-signed-zeros -fno-math-errno -fno-trapping-math -ffast-math
# CC_FLAGS = -g -fopenmp  -O2  --use-clang -std=c90
#CC_FLAGS = -g -fopenmp  -O2  --use-clang -std=c90


backprop: backprop.o facetrain.o imagenet.o backprop_kernel.o
	$(CC) $(CC_FLAGS) backprop.o facetrain.o imagenet.o backprop_kernel.o -o backprop -lm

%.o: %.[ch]
	$(CC) $(CC_FLAGS) $< -c

facetrain.o: facetrain.c backprop.h
	$(CC) $(CC_FLAGS) facetrain.c -c -o facetrain.o
    
backprop.o: backprop.c backprop.h
	$(CC) $(CC_FLAGS) backprop.c -c -o backprop.o

backprop_kernel.o: backprop_kernel.c backprop.h
	$(CC) $(CC_FLAGS) backprop_kernel.c -c -o backprop_kernel.o

imagenet.o: imagenet.c backprop.h
	$(CC) $(CC_FLAGS) imagenet.c -c -o imagenet.o


clean:
	rm -f *.o *~ backprop backprop_cuda.linkinfo
