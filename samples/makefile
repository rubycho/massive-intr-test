CC=gcc
CFLAGS=-lrt -pthread

all: massive_intr massive_intr_1

massive_intr:
	$(CC) -o massive_intr massive_intr.c $(CFLAGS)

massive_intr_1:
	$(CC) -o massive_intr_1 massive_intr_1.c $(CFLAGS)

clean:
	rm -f massive_intr massive_intr_1
