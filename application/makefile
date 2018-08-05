CC=gcc
CFLAGS=-lrt -pthread

all: massive_intr

massive_intr:
	$(CC) -o massive_intr massive_intr.c parser.c inih/ini.c $(CFLAGS)

clean:
	rm -f massive_intr
