#ifndef ARRAY_H
#define ARRAY_H

#include <stdint.h>

typedef struct {
    float *array;
    uint16_t len;
    uint16_t size;
} ArrayFloat;

ArrayFloat* newArrayFloat(uint16_t len);
int addFloat(ArrayFloat *array, float value);

#endif