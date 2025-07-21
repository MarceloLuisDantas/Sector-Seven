#include <stdlib.h>

typedef struct Array {
    int *array;
    size_t len;
    size_t max;
} Array;

Array *newArray(size_t len) {
    Array *ar = malloc(sizeof(array));
    ar->array = malloc(sizeof(int) * len);
    ar->max = len;
    ar->len = 0;
    return ar;
}

Array *concat(const Array *a1, const Array *a2) {
    Array *ar = malloc(sizeof(array));
    ar->array = malloc(sizeof(int) * (a1->max + a2->max));
    
    int count = 0;
    for (int i = 0; i < a1->len; i++) {
        ar->array[count] = a1->array[i];
        count += 1;
    }

    for (int i = 0; i < a2->len; i++) {
        ar->array[count] = a2->array[i];
        count += 1;
    }
    
    ar->len = count;
    ar->max = a1->max + a2->max;
    return ar;
}

