#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct {
    float *array;
    uint16_t len;
    uint16_t size;
} ArrayFloat;

ArrayFloat* newArrayFloat(uint16_t len) {
    ArrayFloat *ar = malloc(sizeof(ArrayFloat));
    ar->array = malloc(sizeof(int) * len);
    ar->size = len;
    ar->len = 0;
    return ar;
}

int addFloat(ArrayFloat *array, float value) {
    if (array->len >= array->size)
        return 0;

    array->array[array->len] = value;
    array->len += 1;
    return 1;
}