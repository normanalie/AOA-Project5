# Répertoires de sortie
BINDIR = bin
OBJDIR = obj

# Compilateur et options
CC = clang
CFLAGS = -O2 -g -Wall
OPTFLAGS = -O3 -g -Wall
LDFLAGS = -lm

# Fichiers objets communs
OBJS_COMMON = $(OBJDIR)/kernel.o $(OBJDIR)/rdtsc.o

.PHONY: all clean directories

all: directories $(BINDIR)/check $(BINDIR)/calibrate $(BINDIR)/measure

directories:
	mkdir -p $(BINDIR) $(OBJDIR)

$(BINDIR)/check: $(OBJS_COMMON) $(OBJDIR)/driver_check.o
	$(CC) -o $@ $^ $(LDFLAGS)

$(BINDIR)/calibrate: $(OBJS_COMMON) $(OBJDIR)/driver_calib.o
	$(CC) -o $@ $^ $(LDFLAGS)

$(BINDIR)/measure: $(OBJS_COMMON) $(OBJDIR)/driver.o
	$(CC) -o $@ $^ $(LDFLAGS)

$(OBJDIR)/driver_check.o: driver_check.c
	$(CC) $(CFLAGS) -D CHECK -c $< -o $@

$(OBJDIR)/driver_calib.o: driver_calib.c
	$(CC) $(CFLAGS) -D CALIB -c $< -o $@

$(OBJDIR)/driver.o: driver.c
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJDIR)/kernel.o: kernel.c
	$(CC) $(OPTFLAGS) -D $(OPT) -c $< -o $@

$(OBJDIR)/rdtsc.o: rdtsc.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(OBJDIR) $(BINDIR)
