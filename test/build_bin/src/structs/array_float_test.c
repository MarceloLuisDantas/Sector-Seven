#include <stdio.h>

#include "array_float.h"

int main() {

    ArrayFloat *af = newArrayFloat(5);
    int x = addFloat(af, 10.2);

    if(af->array[0] == 10.1)
        printf("Ok float");
    else 
        printf("%f\n", af->array[0]);

    return 0;
}