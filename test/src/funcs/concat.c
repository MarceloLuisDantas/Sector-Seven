#include "../structs/array_int.h"
#include <stdlib.h>
#include <stdint.h>

Array *concat(Array *a1, Array *a2) {
    uint16_t new_len = a1->size + a2->size;
    Array *a3 = newArray(new_len);

    for (uint16_t i = 0; i < a1->len; i++) 
        add(a3, a1->array[i]);
    
    for (uint16_t i = 0; i < a2->len; i++) 
        add(a3, a2->array[i]);
    
    return a3;
}
