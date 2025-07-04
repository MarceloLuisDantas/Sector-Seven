#include <stdio.h>
#include <stdlib.h>
#include "structs/array_int.h"
#include "structs/array_float.h"
#include "funcs/concat.h"

int main() {
    Array *a1 = newArray(5);
    add(a1, 1);
    add(a1, 2);

    Array *a2 = newArray(5);
    add(a2, 5);
    add(a2, 6);

    Array *a3 = concat(a1, a2);
    for (int i = 0; i < a3->len; i++) {
        printf("Element: %i = %i\n", i, a3->array[i]);
    }
    
    ArrayFloat *af = newArrayFloat(5);
    addFloat(af, 2.3);
    printf("%f\n", af->array[0]);

    return 0;
}
