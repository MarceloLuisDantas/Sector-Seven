#include <stdlib.h>
#include <stdbool.h>

typedef struct Array {
    int *array;
    int size;
    int len;
} Array;

Array *new_array(int len) {
    Array *a = malloc(sizeof(Array));
    a->array = malloc(sizeof(int) * len);
    a->size = len;
    a->len = 0;
    return a;
}

Array *concat(Array *a1, Array *a2) {
    Array *a3 = new_array(a1->size + a2->size);
    int a3_count = 0;
    for (int i = 0; i < a1->size; i++) {
        a3->array[a3_count] = a1->array[i];
        a3_count += 1;
    }
    for (int i = 0; i < a2->size; i++) {
        a3->array[a3_count] = a2->array[i];
        a3_count += 1;
    }
    a3->len = a1->len + a2->len;
    return a3;
}

bool add(Array *self, int value) {
    if (self->size == self->len) 
        return false;
    
    self->array[self->len] = value;
    self->len += 1;
    return false;
}