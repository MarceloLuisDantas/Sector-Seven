#include <stdio.h>
#include <stdlib.h>

int seg_fault() {
    char *value;
    for (int i = 0; i != 2000; i++)
        value[i] = 1;
}