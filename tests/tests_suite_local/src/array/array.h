#ifndef ARRAY_H
#define ARRAY_H

    #include <stdbool.h>

    typedef struct Array {
        int *array;
        int size;
        int len;
    } Array;

    Array *new_array(int len);
    Array *concat(Array *a1, Array *a2);
    bool add(Array *self, int value);

#endif