#include <stdio.h>

#include "array_int.h"

int main() {
    Array *ai = newArray(5);
    int x = add(ai, 10);

    if(ai->array[0] == 10)
        printf("Ok int");
}