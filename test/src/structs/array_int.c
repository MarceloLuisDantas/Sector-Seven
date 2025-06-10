#include <stdint.h>
#include <stdlib.h>

typedef struct {
    int *array;
    uint16_t len;
    uint16_t size;
} Array;

Array* newArray(uint16_t len) {
    Array *ar = malloc(sizeof(Array));
    ar->array = malloc(sizeof(int) * len);
    ar->size = len;
    ar->len = 0;
    return ar;
}

int add(Array *array, int value) {
    if (array->len >= array->size)
        return 0;

    array->array[array->len] = value;
    array->len += 1;
    return 1;
}