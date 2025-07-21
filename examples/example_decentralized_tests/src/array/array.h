#ifndef ARRAY_H
#define ARRAY_H

typedef struct Array {
    int *array;
    size_t len;
    size_t max;
} Array;

Array *newArray(size_t len);
Array *concat(const Array *a1, const Array *a2);

#endif