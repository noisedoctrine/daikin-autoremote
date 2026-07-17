CC = gcc
CFLAGS = -Wall -O2
LDFLAGS = -lpigpio -lrt -lpthread

SRC = src/main.c src/daikin_arc480.c
OBJ = $(SRC:.c=.o)
TARGET = daikin_ir

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)

.PHONY: all clean
