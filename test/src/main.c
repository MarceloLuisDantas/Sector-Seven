#include <stdio.h>
#include <stdlib.h>
#include "structs/array_int.h"
#include "funcs/concat.h"

int main() {

    Array *a1 = newArray(5);
    add(a1, 1);
    add(a1, 2);
    add(a1, 3);
    add(a1, 4);

    Array *a2 = newArray(5);
    add(a2, 5);
    add(a2, 6);
    add(a2, 7);
    add(a2, 8);

    Array *a3 = concat(a1, a2);

    for (int i = 0; i < a3->len; i++) {
        printf("Elemento: %i = %i\n", i, a3->array[i]);
    }
    
    return 0;
}
