CC = gcc
CFLAGS = -O2 -Wall -I .

# This flag includes the Pthreads library on a Linux box.
# Others systems will probably require something different.
LIB = -lpthread

all: tinys tinyp tinyt cgi

tinys: tinys.c csapp.o
	$(CC) $(CFLAGS) -o tinys tinys.c csapp.o $(LIB)

tinyp: tinyp.c csapp.o
	$(CC) $(CFLAGS) -o tinyp tinyp.c csapp.o $(LIB)

tinyt: tinyt.c csapp.o
	$(CC) $(CFLAGS) -o tinyt tinyt.c csapp.o $(LIB)

csapp.o: csapp.c
	$(CC) $(CFLAGS) -c csapp.c

cgi:
	(cd cgi-bin; make)

clean:
	rm -f *.o tiny *~
	(cd cgi-bin; make clean)

