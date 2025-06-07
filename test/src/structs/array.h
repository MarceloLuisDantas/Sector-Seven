#ifndef ARRAY_H
#define ARRAY_H

#include <stdint.h>

typedef struct {
    int *array;
    uint16_t len;
    uint16_t size;
} Array;

Array* newArray(uint16_t len);
int add(Array *array, int value);

#endif